#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <limits>

using namespace std;

struct Employee {
    string fullName;
    struct BirthDate {
        int day, month, year;
    };
    BirthDate birthDate;
    int experienceYears;
    double salary;
};

auto compareByBirthDate = [](const Employee& a, const Employee& b) {
    return a.birthDate.year < b.birthDate.year ||
           (a.birthDate.year == b.birthDate.year && a.birthDate.month < b.birthDate.month) ||
           (a.birthDate.year == b.birthDate.year && a.birthDate.month == b.birthDate.month &&
            a.birthDate.day < b.birthDate.day);
};

int main() {
    int n;
    cout << "Введите количество сотрудников: ";
    cin >> n;

    vector<Employee> employees(n);

    for(auto& e : employees) {
        cout << "ФИО: ";
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        getline(cin, e.fullName);                       
        cout << "Дата рождения: ";
        cin >> e.birthDate.day >> e.birthDate.month >> e.birthDate.year;
        cout << "Стаж работы: ";
        cin >> e.experienceYears;
        cout << "Оклад: ";
        cin >> e.salary;
    }

    sort(employees.begin(), employees.end(), compareByBirthDate);

    cout << "\nСортировка по дате рождения:" << endl;
    for(const auto& e : employees) {
        cout << e.fullName << ", " << e.birthDate.day << '.' << e.birthDate.month << '.' << e.birthDate.year << endl;
    }

    auto [minExp, maxExp] = minmax_element(employees.begin(), employees.end(),
                                           [](const Employee& a, const Employee& b){
                                               return a.experienceYears < b.experienceYears;
                                           });

    cout << "\nМинимальный стаж: " << (*minExp).experienceYears << " лет" << endl;
    cout << "Максимальный стаж: " << (*maxExp).experienceYears << " лет" << endl;

    double avgSalary = accumulate(employees.begin(), employees.end(), 0.0,
                                  [](double acc, const Employee& e){ return acc + e.salary; }) /
                       employees.size();

    cout << "Средний оклад по фирме: " << avgSalary << endl;

    return 0;
}
