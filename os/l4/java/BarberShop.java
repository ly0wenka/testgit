import java.util.concurrent.Semaphore;

public class BarberShop {
    static final int NUM_CHAIRS = 3;
    static final int NUM_CLIENTS = 10;

    static Semaphore barberSleep = new Semaphore(0);
    static Semaphore chair = new Semaphore(1);
    static Semaphore waitingRoom = new Semaphore(NUM_CHAIRS);
    static Semaphore haircutDone = new Semaphore(0);

    static class Barber extends Thread {
        public void run() {
            while (true) {
                try {
                    barberSleep.acquire();
                    System.out.println("Barber is cutting a client's hair...");
                    Thread.sleep(3000);
                    System.out.println("Barber finished the haircut.");
                    haircutDone.release();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    static class Client extends Thread {
        int id;
        Client(int id) { this.id = id; }

        public void run() {
            System.out.println("Client " + id + " arrived.");
            if (waitingRoom.tryAcquire()) {
                System.out.println("Client " + id + " is sitting in the waiting room.");
                try {
                    chair.acquire();
                    barberSleep.release(); // Wake up the barber
                    haircutDone.acquire(); // Wait for the haircut to finish
                    chair.release();
                    waitingRoom.release();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            } else {
                System.out.println("Client " + id + " leaves because no seats are available.");
            }
        }
    }

    public static void main(String[] args) {
        new Barber().start();

        for (int i = 1; i <= NUM_CLIENTS; i++) {
            new Client(i).start();
            try { Thread.sleep(1000); } catch (InterruptedException e) {}
        }
    }
}
