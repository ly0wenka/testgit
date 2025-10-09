public class Main {
    public static void main(String[] args) {
        while (true) {
            System.out.println("Hello, World!");
            try {
                Thread.sleep(5000); // wait for 5000 milliseconds = 5 seconds
            } catch (InterruptedException e) {
                System.err.println("Sleep interrupted");
            }
        }
    }
}