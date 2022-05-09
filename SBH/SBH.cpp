#include <iostream>
#include <fstream>
#include <string>

#define _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_DEPRECATE
#pragma warning(disable : 4996)

char generate() {
    char data[4] = { 'A', 'C', 'G', 'T' };
    int range = 3 - 0 + 1;
    int num = rand() % range;
    return data[num];
}

void generateToFile(int n) {
    char* sequence = new char[n];

    std::ofstream MyFile("sequence.txt");
    for (int i = 0; i < n; i++) {
        sequence[i] = generate();
        MyFile << sequence[i];
    }
    MyFile.close();

    delete[] sequence;
}

std::string readFromFile() {
    std::string myText;
    std::ifstream MyReadFile("sequence.txt");
    while (std::getline(MyReadFile, myText)) {
        std::cout << myText;
    }
    MyReadFile.close();
    return myText;
}

int main()
{
    int n = 500;
    
    generateToFile(n);
    std::string str = readFromFile();

    char* sequence = new char[str.length() + 1];

    strcpy(sequence, str.c_str());
    for (int i = 0; i < str.length(); i++) {
        std::cout << sequence[i];
    }

    delete[] sequence;
}

