#include <vector>

template <typename T>
T sum_vector(const std::vector<T>& data) {
    T total = {};
    for (const auto& item : data) {
        total += item;
    }
    return total;
}

inline double mul(double a, double b) {
    return a * b;
}
