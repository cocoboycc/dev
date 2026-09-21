#include <iostream>
#include <algorithm>
#include <vector>
#include <cassert>

// function to determine whether bit position is 0 or 1
char bit_checker(const std::string& A, int bit) {
    return A[bit];
}

// insertion of strings with binary 0 or 1
void radix_sort(std::vector<std::string>& vec, int left, int right, int bit) {

    if (left >= right || bit < 0) {
        return;
    }

    assert(static_cast<size_t>(bit) < vec[0].size());

    int i = left-1;
    int j = right+1;

    do {
        do {
            ++i;
        } while (i < j && bit_checker(vec[i], bit) == '0');

        do {
            --j;
        } while (i < j && bit_checker(vec[j], bit) == '1');

        if (i < j) {
            std::swap(vec[i], vec[j]);
        }

    } while (i < j);

    radix_sort(vec, left, i - 1, bit + 1);
    radix_sort(vec, i, right, bit + 1);
}

int main() {

    std::vector<std::string> vec = {
        "101",
        "010",
        "110",
        "001"
    };

    radix_sort(vec, 0, vec.size() - 1, 0);

    for (const auto& s : vec) {
        std::cout << s << " ";
    }

    return 0;
}