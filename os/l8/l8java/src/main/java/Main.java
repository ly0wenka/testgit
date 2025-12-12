import org.apache.poi.xwpf.usermodel.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main {

    public static void main(String[] args) throws Exception {

        Path folder = Paths.get("S:/Users/L/Downloads/New folder (175)/testgit/os/l8/imgs");
        List<Path> images = new ArrayList<>();

        DirectoryStream.Filter<Path> filter = entry -> {
            String ext = entry.toString().toLowerCase();
            return ext.endsWith(".png") || ext.endsWith(".jpg") || ext.endsWith(".jpeg")
                    || ext.endsWith(".bmp") || ext.endsWith(".gif");
        };

        try (DirectoryStream<Path> ds = Files.newDirectoryStream(folder, filter)) {
            ds.forEach(images::add);
        }

        images.sort(Comparator.comparing(Path::toString));

        XWPFDocument doc = new XWPFDocument();
        int index = 1;

        for (Path img : images) {

            String name = img.getFileName().toString();
            String stem = name.substring(0, name.lastIndexOf('.'));

            // reference text
            XWPFParagraph p1 = doc.createParagraph();
            p1.setAlignment(ParagraphAlignment.BOTH);
            p1.createRun().setText("На рис. " + index + " зображено " + stem + ".");

            // image
            XWPFParagraph pImg = doc.createParagraph();
            pImg.setAlignment(ParagraphAlignment.CENTER);

            XWPFRun rImg = pImg.createRun();
            try (InputStream is = Files.newInputStream(img)) {
                rImg.addPicture(is, XWPFDocument.PICTURE_TYPE_JPEG, name,
                        500 * 9525, 350 * 9525); // px → EMU
            }

            // caption
            XWPFParagraph cap = doc.createParagraph();
            cap.setAlignment(ParagraphAlignment.CENTER);
            cap.createRun().setText("Рис. " + index + " — " + stem);

            index++;
        }

        try (FileOutputStream fos = new FileOutputStream(folder.resolve("imgs.docx").toString())) {
            doc.write(fos);
        }

        System.out.println("Готово!");
    }
}
