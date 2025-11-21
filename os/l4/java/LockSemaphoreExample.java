public class LockSemaphoreExample {
    private static final Object locker = new Object();
    private static int availableSlots;

    static class Worker extends Thread {
        int id;
        Worker(int id) { this.id = id; }

        public void run() {
            enter();
            try {
                System.out.println("Thread " + id + " entered critical section.");
                Thread.sleep(2000);
                System.out.println("Thread " + id + " leaving critical section.");
            } catch (InterruptedException e) {}
            exit();
        }

        void enter() {
            synchronized (locker) {
                while (availableSlots == 0) {
                    try { locker.wait(); } catch (InterruptedException e) {}
                }
                availableSlots--;
            }
        }

        void exit() {
            synchronized (locker) {
                availableSlots++;
                locker.notify(); // повідомляємо один потік
            }
        }
    }

    public static void main(String[] args) {
        int maxSlots = 2;
        availableSlots = maxSlots;

        for (int i = 1; i <= 5; i++) {
            new Worker(i).start();
        }
    }
}
