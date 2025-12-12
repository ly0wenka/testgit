#include <pugixml.hpp>
#include <zip.h>
#include <fstream>
#include <string>

int main() {
    // XML для document.xml
    const char* docXml = R"(
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:body>
        <w:p>
          <w:r>
            <w:t>Hello from C++ DOCX!</w:t>
          </w:r>
        </w:p>
      </w:body>
    </w:document>
    )";

    // Створюємо архів DOCX (ZIP)
    int err = 0;
    zip_t* zip = zip_open("test.docx", ZIP_CREATE | ZIP_TRUNCATE, &err);
    zip_source_t* src = zip_source_buffer(zip, docXml, strlen(docXml), 0);
    zip_file_add(zip, "word/document.xml", src, ZIP_FL_OVERWRITE);
    zip_close(zip);

    return 0;
}