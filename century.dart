void main() {
  final years = [1705, 1900, 1601, 2000];

  for(final year in years) {
    final century = calculateCentury(year);
    print(century); // вывод результата
  }
}

// Функция расчета века по заданному году
int calculateCentury(final int year) {
  return ((year - 1) ~/ 100) + 1;
}
