#include <windows.h>
#include <fstream>
#include <string>
#include <vector>
#include <iostream>
#include <algorithm>

void writeFile(const std::string& path, const std::string& content) {
    std::ofstream f(path, std::ios::binary);
    f << content;
    f.close();
}

bool copyFile(const std::string& src, const std::string& dest) {
    return CopyFileA(src.c_str(), dest.c_str(), FALSE) != 0;
}

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
                std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
                if (ext == "png" || ext == "jpg" || ext == "jpeg") {
                    files.push_back(folder + "\\" + name);
                }
            }
        }
    } while (FindNextFileA(hFind, &ffd));
    FindClose(hFind);
    return files;
}

int main() {
    // Шлях до ваших картинок
    std::string imgFolder = "S:\\Users\\L\\Downloads\\New folder (175)\\testgit\\os\\l8\\imgs";
    std::string temp = "docx_temp";

    // 1. Створення структури папок
    system(("rmdir /s /q " + temp + " >nul 2>&1").c_str()); // Очищення старої папки
    system(("mkdir " + temp).c_str());
    system(("mkdir " + temp + "\\_rels").c_str());
    system(("mkdir " + temp + "\\docProps").c_str());
    system(("mkdir " + temp + "\\word").c_str());
    system(("mkdir " + temp + "\\word\\media").c_str());
    system(("mkdir " + temp + "\\word\\_rels").c_str());

    auto images = listImages(imgFolder);
    if (images.empty()) {
        std::cout << "Зображень не знайдено за вказаним шляхом!\n";
        return 1;
    }

    std::vector<std::string> names;
    for (size_t i = 0; i < images.size(); i++) {
        std::string ext = images[i].substr(images[i].find_last_of('.'));
        std::string name = "image" + std::to_string(i + 1) + ext;
        copyFile(images[i], temp + "\\word\\media\\" + name);
        names.push_back(name);
    }

    // 2. document.xml (з вашим форматуванням)
    std::string docXml = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\" "
        "xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">"
        "<w:body>";

    docXml += "<w:p><w:pPr><w:pStyle w:val=\"Heading1\"/></w:pPr><w:r><w:rPr>"
        "<w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:sz w:val=\"32\"/>"
        "</w:rPr><w:t>Звіт з зображеннями</w:t></w:r></w:p>";

    for (size_t i = 0; i < names.size(); i++) {
        // Текст перед фото
        docXml += "<w:p><w:pPr><w:jc w:val=\"both\"/></w:pPr><w:r><w:rPr>"
            "<w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:sz w:val=\"28\"/>"
            "</w:rPr><w:t>На рис. " + std::to_string(i + 1) + " зображено " + names[i] + "</w:t></w:r></w:p>";

        // Сама картинка
        docXml += "<w:p><w:r><w:drawing><wp:inline><wp:extent cx=\"1905000\" cy=\"1905000\"/>"
            "<wp:docPr id=\"" + std::to_string(i + 1) + "\" name=\"Pic" + std::to_string(i + 1) + "\"/>"
            "<a:graphic><a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">"
            "<pic:pic><pic:nvPicPr><pic:cNvPr id=\"" + std::to_string(i + 1) + "\" name=\"img" + std::to_string(i + 1) + "\"/><pic:cNvPicPr/></pic:nvPicPr>"
            "<pic:blipFill><a:blip r:embed=\"rId" + std::to_string(i + 1) + "\"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>"
            "<pic:spPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"1905000\" cy=\"1905000\"/></a:xfrm><a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom></pic:spPr>"
            "</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>";

        // Підпис
        docXml += "<w:p><w:pPr><w:jc w:val=\"center\"/></w:pPr><w:r><w:rPr>"
            "<w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\"/><w:sz w:val=\"28\"/>"
            "</w:rPr><w:t>Рис. " + std::to_string(i + 1) + " — " + names[i] + "</w:t></w:r></w:p>";
    }
    docXml += "</w:body></w:document>";
    writeFile(temp + "\\word\\document.xml", docXml);

    // 3. Допоміжні XML файли (Обов'язкові для відкриття в Word)
    std::string rels = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">";
    for (size_t i = 0; i < names.size(); i++)
        rels += "<Relationship Id=\"rId" + std::to_string(i + 1) + "\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" Target=\"media/" + names[i] + "\"/>";
    rels += "</Relationships>";
    writeFile(temp + "\\word\\_rels\\document.xml.rels", rels);

    writeFile(temp + "\\_rels\\.rels", "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/><Relationship Id=\"rId2\" Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" Target=\"docProps/core.xml\"/></Relationships>");
    writeFile(temp + "\\docProps\\core.xml", "<?xml version=\"1.0\" encoding=\"UTF-8\"?><cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/core-properties\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\"></cp:coreProperties>");

    writeFile(temp + "\\[Content_Types].xml", "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\"><Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/><Default Extension=\"xml\" ContentType=\"application/xml\"/><Default Extension=\"png\" ContentType=\"image/png\"/><Default Extension=\"jpg\" ContentType=\"image/jpeg\"/><Default Extension=\"jpeg\" ContentType=\"image/jpeg\"/><Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/></Types>");

    // 4. Правильне пакування (Використовуємо -LiteralPath і перехід у папку)
    system("del result.docx >nul 2>&1");
    // Важливо: зайти в папку, щоб файли були в корені архіву
    system("powershell -Command \"Set-Location docx_temp; Compress-Archive -Path * -DestinationPath ..\\result.zip -Force\"");
    system("rename result.zip result.docx");

    std::cout << "✔ Файл result.docx створено успішно!\n";
    return 0;
}