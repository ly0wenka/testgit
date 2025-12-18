#include <windows.h>
#include <fstream>
#include <string>
#include <iostream>

void writeFile(const std::string& path, const std::string& content) {
    std::ofstream f(path, std::ios::binary);
    f << content;
    f.close();
}

bool copyFile(const std::string& src, const std::string& dest) {
    return CopyFileA(src.c_str(), dest.c_str(), FALSE) != 0;
}

int main() {
    // Шлях до твоєї картинки
    std::string imagePath = "S:\\Users\\L\\Downloads\\New folder (175)\\testgit\\os\\l8\\imgs\\Screenshot_1.png"; // має існувати поруч з exe
    std::string tempDir = "docx_temp";

    // Створюємо папки
    system(("mkdir " + tempDir).c_str());
    system(("mkdir " + tempDir + "\\_rels").c_str());
    system(("mkdir " + tempDir + "\\docProps").c_str());
    system(("mkdir " + tempDir + "\\word").c_str());
    system(("mkdir " + tempDir + "\\word\\_rels").c_str());
    system(("mkdir " + tempDir + "\\word\\media").c_str());

    // Копіюємо картинку у word/media
    copyFile(imagePath, tempDir + "\\word\\media\\image1.png");

    // Створюємо word/document.xml з одним малюнком
    writeFile(tempDir + "\\word\\document.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" "
        "xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">\n"
        "  <w:body>\n"
        "    <w:p>\n"
        "      <w:r>\n"
        "        <w:drawing>\n"
        "          <wp:inline>\n"
        "            <wp:extent cx=\"1905000\" cy=\"1905000\"/>\n" // Розмір в EMU (952500 = 1 дюйм)
        "            <wp:docPr id=\"1\" name=\"Picture 1\"/>\n"
        "            <a:graphic>\n"
        "              <a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">\n"
        "                <pic:pic>\n"
        "                  <pic:nvPicPr>\n"
        "                    <pic:cNvPr id=\"0\" name=\"image1.png\"/>\n"
        "                    <pic:cNvPicPr/>\n"
        "                  </pic:nvPicPr>\n"
        "                  <pic:blipFill>\n"
        "                    <a:blip r:embed=\"rId1\"/>\n"
        "                    <a:stretch><a:fillRect/></a:stretch>\n"
        "                  </pic:blipFill>\n"
        "                  <pic:spPr>\n"
        "                    <a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"1905000\" cy=\"1905000\"/></a:xfrm>\n"
        "                    <a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom>\n"
        "                  </pic:spPr>\n"
        "                </pic:pic>\n"
        "              </a:graphicData>\n"
        "            </a:graphic>\n"
        "          </wp:inline>\n"
        "        </w:drawing>\n"
        "      </w:r>\n"
        "    </w:p>\n"
        "  </w:body>\n"
        "</w:document>"
    );

    // Створюємо word/_rels/document.xml.rels
    writeFile(tempDir + "\\word\\_rels\\document.xml.rels",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">\n"
        "  <Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" Target=\"media/image1.png\"/>\n"
        "</Relationships>"
    );

    // Створюємо docProps/core.xml
    writeFile(tempDir + "\\docProps\\core.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\"/>\n"
    );

    // Створюємо docProps/app.xml
    writeFile(tempDir + "\\docProps\\app.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\">\n"
        "  <Application>Microsoft Office Word</Application>\n"
        "</Properties>\n"
    );

    // Створюємо _rels/.rels
    writeFile(tempDir + "\\_rels\\.rels",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">\n"
        "  <Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>\n"
        "  <Relationship Id=\"rId2\" Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" Target=\"docProps/core.xml\"/>\n"
        "  <Relationship Id=\"rId3\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties\" Target=\"docProps/app.xml\"/>\n"
        "</Relationships>"
    );

    // Створюємо [Content_Types].xml
    writeFile(tempDir + "\\[Content_Types].xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">\n"
        "  <Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>\n"
        "  <Default Extension=\"xml\" ContentType=\"application/xml\"/>\n"
        "  <Default Extension=\"png\" ContentType=\"image/png\"/>\n"
        "  <Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>\n"
        "  <Override PartName=\"/docProps/core.xml\" ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/>\n"
        "  <Override PartName=\"/docProps/app.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.extended-properties+xml\"/>\n"
        "</Types>\n"
    );

    // Створюємо zip і перейменовуємо у docx
    system("powershell Compress-Archive -Path docx_temp\\* -DestinationPath doc_with_image.zip -Force");
    system("rename doc_with_image.zip doc_with_image.docx");

    std::cout << "Файл doc_with_image.docx створено з однією картинкою!" << std::endl;
    return 0;
}
