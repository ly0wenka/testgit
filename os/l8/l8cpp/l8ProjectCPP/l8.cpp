#include <windows.h>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>

// Створення папки (wide string)
void createFolder(const std::wstring& path) {
    CreateDirectoryW(path.c_str(), NULL);
}

// Копіювання файлу (wide string)
bool copyFile(const std::wstring& src, const std::wstring& dest) {
    return CopyFileW(src.c_str(), dest.c_str(), FALSE) != 0;
}

// Список файлів у теці
std::vector<std::wstring> listFiles(const std::wstring& folder) {
    std::vector<std::wstring> files;
    WIN32_FIND_DATAW findFileData;
    HANDLE hFind = FindFirstFileW((folder + L"\\*").c_str(), &findFileData);
    if (hFind == INVALID_HANDLE_VALUE) return files;

    do {
        if (!(findFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            files.push_back(folder + L"\\" + findFileData.cFileName);
        }
    } while (FindNextFileW(hFind, &findFileData) != 0);
    FindClose(hFind);
    return files;
}

// Генерація document.xml
std::string createDocumentXml(int count) {
    std::ostringstream xml;
    xml << R"(<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
)";
    for (int i = 1; i <= count; ++i) {
        xml << "    <w:p>\n"
            "      <w:r>\n"
            "        <w:drawing>\n"
            "          <wp:inline>\n"
            "            <a:graphic xmlns:a=\"http://schemas.openxmlformats.org/drawingml/2006/main\">\n"
            "              <a:graphicData uri=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">\n"
            "                <pic:pic xmlns:pic=\"http://schemas.openxmlformats.org/drawingml/2006/picture\">\n"
            "                  <pic:blipFill>\n"
            "                    <a:blip r:embed=\"rId" << i << "\"/>\n"
            "                  </pic:blipFill>\n"
            "                </pic:pic>\n"
            "              </a:graphicData>\n"
            "            </a:graphic>\n"
            "          </wp:inline>\n"
            "        </w:drawing>\n"
            "      </w:r>\n"
            "    </w:p>\n";
    }
    xml << "  </w:body>\n</w:document>";
    return xml.str();
}

// Генерація document.xml.rels
std::string createRelsXml(int count, const std::vector<std::wstring>& files) {
    std::ostringstream xml;
    xml << R"(<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
)";
    for (int i = 1; i <= count; ++i) {
        std::wstring ext = files[i - 1].substr(files[i - 1].find_last_of(L'.') + 1);
        std::wstring target = L"media/image" + std::to_wstring(i) + L"." + ext;
        char buf[256];
        WideCharToMultiByte(CP_UTF8, 0, target.c_str(), -1, buf, 256, NULL, NULL);
        xml << "    <Relationship Id=\"rId" << i
            << "\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/image\" Target=\""
            << buf << "\"/>\n";
    }
    xml << "</Relationships>";
    return xml.str();
}

int main() {
    std::wstring folder = L"S:\\Users\\L\\Downloads\\New folder (175)\\testgit\\os\\l8\\imgs";
    std::wstring tempDir = L"docx_temp";

    // Створюємо папки
    createFolder(tempDir);
    createFolder(tempDir + L"\\word");
    createFolder(tempDir + L"\\word\\media");
    createFolder(tempDir + L"\\word\\_rels");
    createFolder(tempDir + L"\\_rels");

    // Отримуємо список файлів
    std::vector<std::wstring> files = listFiles(folder);
    if (files.empty()) {
        std::cerr << "У теці немає файлів!" << std::endl;
        return 1;
    }

    // Копіюємо зображення
    for (size_t i = 0; i < files.size(); ++i) {
        std::wstring ext = files[i].substr(files[i].find_last_of(L'.'));
        std::wstring dest = tempDir + L"\\word\\media\\image" + std::to_wstring(i + 1) + ext;
        copyFile(files[i], dest);
    }

    // Створюємо document.xml
    std::ofstream docXml("docx_temp\\word\\document.xml");
    docXml << createDocumentXml((int)files.size());
    docXml.close();

    // Створюємо [Content_Types].xml
    std::ofstream contentTypes("docx_temp\\[Content_Types].xml");
    contentTypes << R"(<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="jpeg" ContentType="image/jpeg"/>
    <Default Extension="png" ContentType="image/png"/>
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/customXml/itemProps1.xml" ContentType="application/vnd.openxmlformats-officedocument.customXmlProperties+xml"/>
    <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
    <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
    <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
    <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
    <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
    <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
    <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
    <Override PartName="/word/stylesWithEffects.xml" ContentType="application/vnd.ms-word.stylesWithEffects+xml"/>
    <Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
    <Override PartName="/word/webSettings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml"/>
</Types>
)";
    contentTypes.close();

    // Створення _rels\.rels
    std::ofstream relsRoot("docx_temp\\_rels\\.rels");
    relsRoot << R"(<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
    <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail" Target="docProps/thumbnail.jpeg"/>
</Relationships>
)";
    relsRoot.close();

    // Створюємо document.xml.rels
    std::ofstream rels("docx_temp\\word\\_rels\\document.xml.rels");
    rels << createRelsXml((int)files.size(), files);
    rels.close();

    // Створюємо .zip
    system("powershell Compress-Archive -Path docx_temp\\* -DestinationPath output.zip -Force");

    // Переіменовуємо zip у docx
    system("rename output.zip output.docx");

    std::cout << "Документ output.docx створено!" << std::endl;
    return 0;
}
