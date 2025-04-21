#include <iostream>

using namespace std;

struct Employee {
    char name[50];               
    int birthday_day;
    int birthday_month;
    int birthday_year; 
    int years_experience;        
    double salary;              
};

bool isBirthdayEarlier(Employee employee1, Employee employee2) {
    if(employee1.birthday_year != employee2.birthday_year)
        return employee1.birthday_year < employee2.birthday_year;
    else if(employee1.birthday_month != employee2.birthday_month)
        return employee1.birthday_month < employee2.birthday_month;
    else
        return employee1.birthday_day < employee2.birthday_day;
}

void bubbleSort(Employee employees[], int count) {
    bool swapped;
    do {
        swapped = false;
        for(int i = 0; i < count - 1; ++i) {
            if (!isBirthdayEarlier(employees[i], employees[i + 1])) {
                Employee temp = employees[i];
                employees[i] = employees[i + 1];
                employees[i + 1] = temp;
                swapped = true;
            }
        }
    } while(swapped);
}

void collectStats(Employee employees[], int count) {
    int minExperience = employees[0].years_experience;
    int maxExperience = employees[0].years_experience;
    double totalSalary = 0.0;

    for(int i = 0; i < count; ++i) {
        if(employees[i].years_experience < minExperience)
            minExperience = employees[i].years_experience;
        if(employees[i].years_experience > maxExperience)
            maxExperience = employees[i].years_experience;
        totalSalary += employees[i].salary;
    }

    double avgSalary = totalSalary / count;

    cout << "Минимальный стаж: " << minExperience << " лет\n"
         << "Максимальный стаж: " << maxExperience << " лет\n"
         << "Средняя зарплата: " << avgSalary << endl;
}

int main() {
    int numEmployees;
    cout << "Введите количество сотрудников: ";
    cin >> numEmployees;

    Employee employees[numEmployees];

    for(int i = 0; i < numEmployees; ++i) {
        cout << "ФИО: ";
        cin >> employees[i].name;

        cout << "Год рождения: ";
        cin >> employees[i].birthday_year;
        
        cout << "Месяц рождения: ";
        cin >> employees[i].birthday_month;
        
        cout << "День рождения: ";
        cin >> employees[i].birthday_day;

        cout << "Опыт работы: ";
        cin >> employees[i].years_experience;

        cout << "Зарплата: ";
        cin >> employees[i].salary;
    }

    bubbleSort(employees, numEmployees);

    cout << "\nСортировка по дате рождения:\n";
    for(int i = 0; i < numEmployees; ++i) {
        cout << "ФИО: " << employees[i].name << ". Дата рождения (День/Месяц/Год): " << employees[i].birthday_day << '/'
             << employees[i].birthday_month << '/' << employees[i].birthday_year << endl;
    }

    collectStats(employees, numEmployees);

    return 0;
}
