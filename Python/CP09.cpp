#include <iostream>
#include <fstream>
#include <vector>
#include <random>

using namespace std;

int main() {
    string filenameF = "file_f.txt";  // Исходный файл
    string filenameG = "file_g.txt";  // Результирующий файл

    default_random_engine gen(random_device{}());
    uniform_int_distribution<> dist(-1000, 1000);  // Генератор случайных чисел [-1000, 1000]

    ofstream fout(filenameF);
    if (!fout.is_open()) {
        cerr << "Ошибка открытия файла " << filenameF << endl;
        return 1;
    }

    for (int i = 0; i < 20; ++i) {
        fout << dist(gen) << endl;
    }
    fout.close();

    ifstream fin(filenameF);
    ofstream gout(filenameG);

    if (!fin || !gout) {
        cerr << "Ошибка открытия файлов." << endl;
        return 1;
    }

    vector<int> numbers;

    int num;
    while (fin >> num) {
        bool found = false;
        for (int existingNum : numbers) {
            if (existingNum == num) {
                found = true;
                break;
            }
        }
        if (!found) {
            numbers.push_back(num);
            gout << num << endl;
        }
    }

    fin.close();
    gout.close();

    return 0;
}
