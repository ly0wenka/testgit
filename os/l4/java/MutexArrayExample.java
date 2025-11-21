import java.util.concurrent.locks.ReentrantLock;

public class MutexArrayExample {
    static ReentrantLock[] slotLocks;
    static int maxSlots = 2;

    static class Worker extends Thread {
        int id;
        Worker(int id) { this.id = id; }

        public void run() {
            int mySlot = -1;
            while (mySlot == -1) {
                for (int i = 0; i < maxSlots; i++) {
                    if (slotLocks[i].tryLock()) { // пробуємо захопити слот
                        mySlot = i;
                        break;
                    }
                }
                if (mySlot == -1) {
                    try { Thread.sleep(50); } catch (InterruptedException e) {}
                }
            }

            try {
                System.out.println("Thread " + id + " entered slot " + mySlot);
                Thread.sleep(2000);
                System.out.println("Thread " + id + " leaving slot " + mySlot);
            } catch (InterruptedException e) {}
            finally {
                slotLocks[mySlot].unlock();
            }
        }
    }

    public static void main(String[] args) {
        slotLocks = new ReentrantLock[maxSlots];
        for (int i = 0; i < maxSlots; i++) slotLocks[i] = new ReentrantLock();

        for (int i = 1; i <= 5; i++) {
            new Worker(i).start();
        }
    }
}
