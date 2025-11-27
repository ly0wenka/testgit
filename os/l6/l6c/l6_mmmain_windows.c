#include <stdio.h>
#include <windows.h>

static size_t SYSTEM_PAGE_SIZE = 0;

void mm_init() {
    SYSTEM_INFO si;
    GetSystemInfo(&si);
    SYSTEM_PAGE_SIZE = si.dwPageSize;
}

static void *mm_get_new_vm_page_from_kernel(int units) {
    void *addr = VirtualAlloc(NULL, units * SYSTEM_PAGE_SIZE, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (addr == NULL) {
        printf("Error: VM Page allocation Failed\n");
        return NULL;
    }
    memset(addr, 0, units * SYSTEM_PAGE_SIZE);
    return addr;
}

static void mm_return_vm_page_to_kernel(void *vm_page, int units) {
    if (!VirtualFree(vm_page, 0, MEM_RELEASE)) {
        printf("Error: Could not free VM page\n");
    }
}

int main(int argc, char **argv) {
    mm_init();
    printf("VM Page size = %lu\n", SYSTEM_PAGE_SIZE);
    void *addr1 = mm_get_new_vm_page_from_kernel(1);
    void *addr2 = mm_get_new_vm_page_from_kernel(1);
    printf("page 1 = %p, page 2 = %p\n", addr1, addr2);
    mm_return_vm_page_to_kernel(addr1, 1);
    mm_return_vm_page_to_kernel(addr2, 1);
    return 0;
}
