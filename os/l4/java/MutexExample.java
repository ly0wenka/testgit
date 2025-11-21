import java.util.concurrent.locks.ReentrantLock;

public class MutexExample {
    static ReentrantLock lock = new ReentrantLock();

    static class Worker extends Thread {
        int id;
        Worker(int id) { this.id = id; }

        public void run() {
            System.out.println("Thread " + id + " is waiting for mutex...");
            lock.lock();
            try {
                System.out.println("Thread " + id + " entered critical section.");
                Thread.sleep(1000);
                System.out.println("Thread " + id + " is leaving critical section.");
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                lock.unlock();
            }
        }
    }

    public static void main(String[] args) {
        for (int i = 1; i <= 3; i++) {
            new Worker(i).start();
        }
    }
}
