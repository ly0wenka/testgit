// Sorter.java
import java.util.*;

public class Sorter {
    // --- Merge sort implementation ---
    public static void mergeSort(int[] arr, int left, int right) {
        if (left >= right) return;

        int mid = (left + right) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }

    private static void merge(int[] arr, int left, int mid, int right) {
        int[] temp = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;

        while (i <= mid && j <= right) {
            temp[k++] = (arr[i] <= arr[j]) ? arr[i++] : arr[j++];
        }
        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];

        System.arraycopy(temp, 0, arr, left, temp.length);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Введіть кількість елементів: ");
        int n = sc.nextInt();

        int[] arr = new int[n];
        System.out.println("Введіть елементи масиву:");
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        mergeSort(arr, 0, n - 1);

        System.out.println("Відсортований масив:");
        for (int x : arr) System.out.print(x + " ");
        System.out.println();
    }
}
