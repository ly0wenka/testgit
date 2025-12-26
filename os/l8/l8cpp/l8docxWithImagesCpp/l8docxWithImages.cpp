#include <windows.h>
#include <fstream>
#include <string>
#include <vector>
#include <iostream>

void writeFile(const std::string& path, const std::string& content) {
    std::ofstream f(path, std::ios::binary);
    f << content;
    f.close();
}

bool copyFile(const std::string& src, const std::string& dest) {
    return CopyFileA(src.c_str(), dest.c_str(), FALSE) != 0;
}

// Отримуємо список файлів PNG або JPG у теці
std::vector<std::string> listImages(const std::string& folder) {
    std::vector<std::string> files;
    WIN32_FIND_DATAA ffd;
    HANDLE hFind = FindFirstFileA((folder + "\\*").c_str(), &ffd);
    if (hFind == INVALID_HANDLE_VALUE) return files;
    do {
        if (!(ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            std::string name = ffd.cFileName;
            size_t dot = name.find_last_of('.');
            if (dot != std::string::npos) {
                std::string ext = name.substr(dot + 1);
                for (auto& c : ext) c = tolower(c);
                if (ext == "png" || ext == "jpg" || ext == "jpeg") {
                    files.push_back(folder + "\\" + name);
                }
            }
        }
    } while (FindNextFileA(hFind, &ffd) != 0);
    FindClose(hFind);
    return files;
}

int main() {
    std::string folder = "S:\\Users\\L\\Downloads\\New folder (175)\\testgit\\os\\l8\\imgs";
    std::string tempDir = "docx_temp";

    // Створюємо папки
    system(("mkdir " + tempDir).c_str());
    system(("mkdir " + tempDir + "\\_rels").c_str());
    system(("mkdir " + tempDir + "\\docProps").c_str());
    system(("mkdir " + tempDir + "\\word").c_str());
    system(("mkdir " + tempDir + "\\word\\_rels").c_str());
    system(("mkdir " + tempDir + "\\word\\media").c_str());

    // Отримуємо список зображень
    std::vector<std::string> images = listImages(folder);
    if (images.empty()) {
        std::cerr << "Немає зображень у теці!" << std::endl;
        return 1;
    }

    // Копіюємо зображення у word/media
    std::vector<std::string> imageNames;
    for (size_t i = 0; i < images.size(); ++i) {
        std::string ext = images[i].substr(images[i].find_last_of('.'));
        std::string dest = tempDir + "\\word\\media\\image" + std::to_string(i + 1) + ext;
        copyFile(images[i], dest);
        imageNames.push_back("image" + std::to_string(i + 1) + ext);
    }

    // Створюємо document.xml
    std::string docXml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" "
        "xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">\n"
        "  <w:body>\n";

    for (size_t i = 0; i < imageNames.size(); ++i) {
        docXml +=
            "    <w:p>\n"
            "      <w:r>\n"
            "        <w:drawing>\n"
            "          <wp:inline>\n"
            "            <wp:extent cx=\"1905000\" cy=\"1905000\"/>\n"
            "            <wp:docPr id=\"" + std::to_string(i + 1) + "\" name=\"Picture " + std::to_string(i + 1) + "\"/>\n"
            "            <a:graphic>\n"
            "              <a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">\n"
            "                <pic:pic>\n"
            "                  <pic:nvPicPr>\n"
            "                    <pic:cNvPr id=\"0\" name=\"" + imageNames[i] + "\"/>\n"
            "                    <pic:cNvPicPr/>\n"
            "                  </pic:nvPicPr>\n"
            "                  <pic:blipFill>\n"
            "                    <a:blip r:embed=\"rId" + std::to_string(i + 1) + "\"/>\n"
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
            "    </w:p>\n";
    }
    docXml += "  </w:body>\n</w:document>";

    writeFile(tempDir + "\\word\\document.xml", docXml);

    // Створюємо word/_rels/document.xml.rels
    std::string relsXml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">\n";
    for (size_t i = 0; i < imageNames.size(); ++i) {
        relsXml += "  <Relationship Id=\"rId" + std::to_string(i + 1) +
            "\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" Target=\"media/" +
            imageNames[i] + "\"/>\n";
    }
    relsXml += "</Relationships>";
    writeFile(tempDir + "\\word\\_rels\\document.xml.rels", relsXml);

    // Створюємо docProps/core.xml
    writeFile(tempDir + "\\docProps\\core.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\"/>\n");

    // Створюємо docProps/app.xml
    writeFile(tempDir + "\\docProps\\app.xml",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Properties xmlns=\"http://schemas.openxmlformats.org/officeDocument/2006/extended-properties\">\n"
        "  <Application>Microsoft Office Word</Application>\n"
        "</Properties>\n");

    // Створюємо _rels/.rels
    writeFile(tempDir + "\\_rels\\.rels",
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">\n"
        "  <Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/>\n"
        "  <Relationship Id=\"rId2\" Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" Target=\"docProps/core.xml\"/>\n"
        "  <Relationship Id=\"rId3\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties\" Target=\"docProps/app.xml\"/>\n"
        "</Relationships>");

    // Створюємо [Content_Types].xml
    std::string contentTypes =
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
        "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">\n"
        "  <Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>\n"
        "  <Default Extension=\"xml\" ContentType=\"application/xml\"/>\n"
        "  <Default Extension=\"png\" ContentType=\"image/png\"/>\n"
        "  <Default Extension=\"jpg\" ContentType=\"image/jpeg\"/>\n"
        "  <Default Extension=\"jpeg\" ContentType=\"image/jpeg\"/>\n"
        "  <Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>\n"
        "  <Override PartName=\"/docProps/core.xml\" ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/>\n"
        "  <Override PartName=\"/docProps/app.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.extended-properties+xml\"/>\n"
        "</Types>\n";
    writeFile(tempDir + "\\[Content_Types].xml", contentTypes);

    // Створюємо zip і перейменовуємо у docx
    system("powershell Compress-Archive -Path docx_temp\\* -DestinationPath doc_with_images.zip -Force");
    system("rename doc_with_images.zip doc_with_images.docx");

    std::cout << "Файл doc_with_images.docx створено з усіма зображеннями!" << std::endl;
    return 0;
}
