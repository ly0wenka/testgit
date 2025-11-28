import mmap
import sys
import ctypes
import struct

# -------------------------------
# Отримання розміру сторінки
# -------------------------------
if sys.platform == 'win32':
    class SYSTEM_INFO(ctypes.Structure):
        _fields_ = [
            ('wProcessorArchitecture', ctypes.c_uint16),
            ('wReserved', ctypes.c_uint16),
            ('dwPageSize', ctypes.c_uint32),
            ('lpMinimumApplicationAddress', ctypes.c_void_p),
            ('lpMaximumApplicationAddress', ctypes.c_void_p),
            ('dwActiveProcessorMask', ctypes.c_void_p),
            ('dwNumberOfProcessors', ctypes.c_uint32),
            ('dwProcessorType', ctypes.c_uint32),
            ('dwAllocationGranularity', ctypes.c_uint32),
            ('wProcessorLevel', ctypes.c_uint16),
            ('wProcessorRevision', ctypes.c_uint16),
        ]

    sys_info = SYSTEM_INFO()
    ctypes.windll.kernel32.GetSystemInfo(ctypes.byref(sys_info))
    SYSTEM_PAGE_SIZE = sys_info.dwPageSize
else:
    import os
    SYSTEM_PAGE_SIZE = os.sysconf("SC_PAGE_SIZE")


# -------------------------------
# Ініціалізація
# -------------------------------
def mm_init():
    print("VM Page size = {} bytes".format(SYSTEM_PAGE_SIZE))


# -------------------------------
# Виділення віртуальної пам'яті
# -------------------------------
def mm_get_new_vm_page_from_kernel(units):
    size = units * SYSTEM_PAGE_SIZE
    try:
        mm = mmap.mmap(-1, size, access=mmap.ACCESS_WRITE)
        print("Allocated {} bytes".format(size))
        return mm
    except Exception as e:
        print("Error: VM Page allocation Failed")
        print(e)
        return None


# -------------------------------
# Повернення пам'яті
# -------------------------------
def mm_return_vm_page_to_kernel(mm_obj):
    try:
        mm_obj.close()
        print("Memory unmapped")
    except Exception as e:
        print("Error: Could not unmap VM page")
        print(e)


# -------------------------------
# Робота з великим масивом
# -------------------------------
def fill_array(mm_obj, n):
    """Записує числа від 0 до n-1 у mmap пам'ять (uint32)"""
    for i in range(n):
        mm_obj.seek(i * 4)
        mm_obj.write(struct.pack('I', i))  # записуємо 4 байти


def read_array(mm_obj, n):
    """Зчитує числа з mmap пам'яті"""
    arr = []
    for i in range(n):
        mm_obj.seek(i * 4)
        val = struct.unpack('I', mm_obj.read(4))[0]
        arr.append(val)
    return arr


# -------------------------------
# Головний блок
# -------------------------------
if __name__ == "__main__":
    mm_init()

    # Виділяємо 1 сторінку (можна збільшити)
    page = mm_get_new_vm_page_from_kernel(1)

    # Скільки чисел вміщається в одну сторінку
    numbers_count = SYSTEM_PAGE_SIZE // 4  # uint32 = 4 bytes

    # Заповнюємо масив
    fill_array(page, numbers_count)
    print("Array filled with numbers 0..{}".format(numbers_count-1))

    # Зчитуємо та перевіряємо перші 10 елементів
    arr = read_array(page, numbers_count)
    print("Elements:", arr)

    mm_return_vm_page_to_kernel(page)
