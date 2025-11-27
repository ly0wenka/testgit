using System;
using System.IO.MemoryMappedFiles;
using System.Runtime.InteropServices;

class Program
{
    static readonly int SYSTEM_PAGE_SIZE = Environment.SystemPageSize;

    static void MmInit()
    {
        Console.WriteLine($"VM Page size = {SYSTEM_PAGE_SIZE}");
    }

    static MemoryMappedViewAccessor MmGetNewVmPageFromKernel(int units)
    {
        try
        {
            int size = units * SYSTEM_PAGE_SIZE;
            var mmf = MemoryMappedFile.CreateNew(null, size);
            var accessor = mmf.CreateViewAccessor();
            byte[] zeroData = new byte[size];
            accessor.WriteArray(0, zeroData, 0, size);
            return accessor;
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error: VM Page allocation Failed");
            Console.WriteLine(ex);
            return null;
        }
    }

    static void MmReturnVmPageToKernel(MemoryMappedViewAccessor accessor)
    {
        try
        {
            accessor.Dispose();
            Console.WriteLine("Memory unmapped");
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error: Could not unmap VM page");
            Console.WriteLine(ex);
        }
    }

    static void Main(string[] args)
    {
        MmInit();
        var page1 = MmGetNewVmPageFromKernel(1);
        var page2 = MmGetNewVmPageFromKernel(1);

        Console.WriteLine($"page1 = {page1?.SafeMemoryMappedViewHandle?.DangerousGetHandle().ToString("X")}");
        Console.WriteLine($"page2 = {page2?.SafeMemoryMappedViewHandle?.DangerousGetHandle().ToString("X")}");
    }
}

