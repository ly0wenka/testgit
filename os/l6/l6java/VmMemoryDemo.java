import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Files;
import java.nio.file.Path;

public class VmMemoryDemo {


// Get system page size
static final int SYSTEM_PAGE_SIZE = 4096; // fallback
static {
    try {
        int ps = sun.misc.Unsafe.getUnsafe().pageSize();
        System.out.println("VM Page size = " + ps);
    } catch (Exception e) {
        System.out.println("VM Page size = " + SYSTEM_PAGE_SIZE);
    }
}

// Allocate new VM page
static MappedByteBuffer getNewVmPageFromKernel(int units) {
    int size = units * SYSTEM_PAGE_SIZE;
    try {
        Path tempFile = Files.createTempFile("vm_page", ".tmp");
        RandomAccessFile raf = new RandomAccessFile(tempFile.toFile(), "rw");
        raf.setLength(size);
        MappedByteBuffer buffer = raf.getChannel().map(FileChannel.MapMode.READ_WRITE, 0, size);
        // Zero-initialize
        for (int i = 0; i < size; i++) {
            buffer.put(i, (byte)0);
        }
        System.out.println("Allocated VM page of size " + size + " bytes");
        return buffer;
    } catch (IOException e) {
        System.out.println("Error: VM Page allocation failed");
        e.printStackTrace();
        return null;
    }
}

// Return VM page (dispose)
static void returnVmPageToKernel(MappedByteBuffer buffer) {
    // In Java, mapped buffers are garbage-collected
    System.out.println("Memory unmapped (handled by GC)");
}

public static void main(String[] args) {
    MappedByteBuffer page1 = getNewVmPageFromKernel(1);
    MappedByteBuffer page2 = getNewVmPageFromKernel(1);

    System.out.println("page1 buffer: " + page1);
    System.out.println("page2 buffer: " + page2);

    returnVmPageToKernel(page1);
    returnVmPageToKernel(page2);
}


}
