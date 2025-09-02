#include <iostream>
using namespace std;

int main() {
	double over = 0.0;
	
	for(int n = 2; n <= 10; n++) {
		over += static_cast<double>(n);
	}
			
	cout << "Sum equal: " << over << endl;
	return 0;
}
