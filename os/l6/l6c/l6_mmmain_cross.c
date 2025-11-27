#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#include <sys/mman.h>
#endif

static size_t SYSTEM_PAGE_SIZE = 0;

void mm_init() {
#ifdef _WIN32
    SYSTEM_INFO si;
    GetSystemInfo(&si);
    SYSTEM_PAGE_SIZE = si.dwPageSize;
#else
    SYSTEM_PAGE_SIZE = sysconf(_SC_PAGESIZE);
#endif
}

static void *mm_get_new_vm_page_from_kernel(int units) {
#ifdef _WIN32
    void *addr = VirtualAlloc(NULL, units * SYSTEM_PAGE_SIZE, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (addr == NULL) {
        printf("Error: VM Page allocation Failed\n");
        return NULL;
    }
#else
    void *addr = mmap(NULL, units * SYSTEM_PAGE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANON, -1, 0);
    if (addr == MAP_FAILED) {
        printf("Error: VM Page allocation Failed\n");
        return NULL;
    }
#endif
    memset(addr, 0, units * SYSTEM_PAGE_SIZE);
    return addr;
}

static void mm_return_vm_page_to_kernel(void *vm_page, int units) {
#ifdef _WIN32
    if (!VirtualFree(vm_page, 0, MEM_RELEASE)) {
        printf("Error: Could not free VM page\n");
    }
#else
    if (munmap(vm_page, units * SYSTEM_PAGE_SIZE) != 0) {
        perror("Error: Could not unmap VM page");
    }
#endif
}

int main(int argc, char **argv) {
    mm_init();
    printf("VM Page size = %zu\n", SYSTEM_PAGE_SIZE);

    void *addr1 = mm_get_new_vm_page_from_kernel(1);
    void *addr2 = mm_get_new_vm_page_from_kernel(1);

    printf("page 1 = %p, page 2 = %p\n", addr1, addr2);

    mm_return_vm_page_to_kernel(addr1, 1);
    mm_return_vm_page_to_kernel(addr2, 1);

    return 0;
}
