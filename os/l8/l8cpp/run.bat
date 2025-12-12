rem gcc l8.cpp "S:\Users\L\Downloads\New folder (175)\testgit\os\l8\l8cpp\pugixml\pugixml-1.13\src\pugixml.cpp" -I"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\l8cpp\pugixml\pugixml-1.13\src" -o l8.exe
gcc l8.cpp pugixml.cpp ^
 -I"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\l8cpp\pugixml\pugixml-1.13\src" ^
 -I"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\l8cpp\libzip\libzip-1.10.0\lib" ^
 -L"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\l8cpp\libzip\libzip-1.10.0\build\lib" ^
 -lzip -o l8.exe

rem gcc l8.cpp -o l8.exe
./l8.exe