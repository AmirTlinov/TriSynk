#include <iostream>

auto add(int a, int b) -> int {
    return a + b;
}

int main() {
    std::cout << "hello trisynk" << std::endl;
    auto sum = add(2, 3);
    std::cout << "sum=" << sum << std::endl;
    return sum == 5 ? 0 : 1;
}
