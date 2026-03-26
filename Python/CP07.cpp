#include <iostream>
#include <string>
#include <cctype>

int maxConsecutiveDigits(const std::string& str) {
    int currentCount = 0;
    int maxCount = 0;

    for(char ch : str) {
        if(isdigit(ch)) {
            currentCount++;
        } else {
            maxCount = std::max(maxCount, currentCount);
            currentCount = 0;                            
        }
    }

    return std::max(maxCount, currentCount);
}

int main() {
    std::string alfabit = "abc85182defg86fdftimdk391";
    std::cout << "Максимальная длина последовательности цифр: "
              << maxConsecutiveDigits(alfabit) << std::endl;
    return 0;
}
