import mmap
import sys

# Get system page size
if sys.platform == 'win32':
    import ctypes

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
    
    print("=== SYSTEM_INFO PARAMETERS ===")
    for field_name, field_type in sys_info._fields_:
        value = getattr(sys_info, field_name)
        print(f"{field_name}: {value}")
        
    SYSTEM_PAGE_SIZE = sys_info.dwPageSize
else:
    import os
    SYSTEM_PAGE_SIZE = os.sysconf("SC_PAGE_SIZE")


def mm_init():
    print("VM Page size = {}".format(SYSTEM_PAGE_SIZE))


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


def mm_return_vm_page_to_kernel(mm_obj):
    try:
        mm_obj.close()
        print("Memory unmapped")
    except Exception as e:
        print("Error: Could not unmap VM page")
        print(e)


if __name__ == "__main__":
    mm_init()
    page1 = mm_get_new_vm_page_from_kernel(1)
    page2 = mm_get_new_vm_page_from_kernel(1)
    print("page1 = {}, page2 = {}".format(hex(id(page1)), hex(id(page2))))
