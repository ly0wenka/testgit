import java.util.concurrent.Semaphore;

public class SemaphoreExample {
    static Semaphore semaphore = new Semaphore(2); // максимум 2 потоки

    static class Worker extends Thread {
        int id;
        Worker(int id) { this.id = id; }

        public void run() {
            try {
                System.out.println("Thread " + id + " is waiting to enter...");
                semaphore.acquire();
                System.out.println("Thread " + id + " entered!");
                Thread.sleep(2000);
                System.out.println("Thread " + id + " is leaving...");
                semaphore.release();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            new Worker(i).start();
        }
    }
}
