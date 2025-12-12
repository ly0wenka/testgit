#using <Aspose.Words.Cpp.dll>
#include <Aspose.Words.Cpp/Model/Documents/Document.h>
#include <Aspose.Words.Cpp/Model/Documents/DocumentBuilder.h>
#include <Aspose.Words.Cpp/Model/Drawing/Image.h>
#include <filesystem>
#include <iostream>

namespace fs = std::filesystem;
using namespace Aspose::Words;

int main() {
    std::string folderPath = R"(S:\Users\L\Downloads\New folder (175)\testgit\os\l8\imgs)";
    Document doc;
    DocumentBuilder builder(&doc);

    // Заголовок
    builder.Writeln(u"Зображення з теки imgs");
    builder.get_Font()->set_Name(u"Arial");
    builder.get_Font()->set_Size(16);

    std::vector<std::string> exts = { ".png", ".jpg", ".jpeg", ".gif", ".bmp" };
    int index = 1;

    for (const auto& entry : fs::directory_iterator(folderPath)) {
        if (entry.is_regular_file()) {
            std::string ext = entry.path().extension().string();
            bool valid = false;
            for (auto& e : exts) if (ext == e) valid = true;
            if (!valid) continue;

            std::string name = entry.path().stem().string();

            // Текст-посилання
            builder.ParagraphFormat->set_Alignment(ParagraphAlignment::Justify);
            builder.Writeln(u"На рис. " + std::to_wstring(index) + u" зображено " + std::wstring(name.begin(), name.end()) + u".");

            // Зображення
            builder.InsertImage(entry.path().string());

            // Підпис під малюнком
            builder.ParagraphFormat->set_Alignment(ParagraphAlignment::Center);
            builder.Writeln(u"Рис. " + std::to_wstring(index) + u" — " + std::wstring(name.begin(), name.end()));

            builder.Writeln(u""); // Відступ
            index++;
        }
    }

    doc.Save(folderPath + "\\imgs.docx");
    std::cout << "Готово: " << folderPath + "\\imgs.docx" << std::endl;
    return 0;
}
