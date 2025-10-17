// Runner.java
import java.io.*;
import java.util.*;

public class Runner {
    public static void main(String[] args) {
        try {
            // Команда для запуску класу Sorter
            ProcessBuilder pb = new ProcessBuilder("java", "Sorter");

            // Перенаправити ввід/вивід у консоль
            pb.inheritIO();

            // Запустити процес
            Process process = pb.start();

            // Дочекатися завершення
            int exitCode = process.waitFor();
            System.out.println("Процес завершено з кодом: " + exitCode);

        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
