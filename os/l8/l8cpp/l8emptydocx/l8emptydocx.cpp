#include <windows.h>
#include <fstream>
#include <string>
#include <iostream>

void writeFile(const std::string& path, const std::string& content) {
    std::ofstream f(path, std::ios::binary);
    f << content;
    f.close();
}

int main() {
    system("mkdir empty_docx");
    system("mkdir empty_docx\\_rels");
    system("mkdir empty_docx\\docProps");
    system("mkdir empty_docx\\word");
    system("mkdir empty_docx\\word\\_rels");

    writeFile("empty_docx\\word\\document.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">\n"
        "  <w:body>\n"
        "    <w:p><w:r><w:t></w:t></w:r></w:p>\n"
        "  </w:body>\n"
        "</w:document>"
    );

    writeFile("empty_docx\\_rels\\.rels",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">\n"
        "  <Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>\n"
        "  <Relationship Id=\"rId2\" Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" Target=\"docProps/core.xml\"/>\n"
        "  <Relationship Id=\"rId3\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties\" Target=\"docProps/app.xml\"/>\n"
        "</Relationships>"
    );

    writeFile("empty_docx\\docProps\\core.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\"/>\n"
    );

    writeFile("empty_docx\\docProps\\app.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\">\n"
        "  <Application>Microsoft Office Word</Application>\n"
        "</Properties>\n"
    );

    writeFile("empty_docx\\word\\_rels\\document.xml.rels",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"/>\n"
    );

    writeFile("empty_docx\\[Content_Types].xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">\n"
        "  <Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>\n"
        "  <Default Extension=\"xml\" ContentType=\"application/xml\"/>\n"
        "  <Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>\n"
        "  <Override PartName=\"/docProps/core.xml\" ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/>\n"
        "  <Override PartName=\"/docProps/app.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.extended-properties+xml\"/>\n"
        "</Types>\n"
    );

    // Створюємо zip і перейменовуємо у docx
    system("powershell Compress-Archive -Path empty_docx\\* -DestinationPath empty.zip -Force");
    system("rename empty.zip empty.docx");

    std::cout << "Пустий файл empty.docx створено!" << std::endl;
    return 0;
}
