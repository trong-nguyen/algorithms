#include <vector>
#include <iostream>
#include <cassert>
#include <cmath>

#define MAX_POSITIVE 1073741824
#define MAX_NEGATIVE -1073741823

int numDigits(int x) {
    int d = 10; // 32 bit - 1(signed)
    while(x < pow(10, --d));
    return d;
}

class Solution {
public:
    int reverse(int x) {
        const int d = numDigits(x);

        int reversed = 0;

        for(int i = d; i >=0; i--) {
            const auto units = pow(10, i);
            int xi = x / units; // note the implitcit conversion
            reversed += x / units * pow(10, d - i);
            x -= units;
            std::cout << x << " " << reversed << "\n";
        }


        if(reversed > MAX_POSITIVE || reversed < MAX_NEGATIVE) {
            //overflow
            return 0;
        } else {
            return reversed;
        }
    }
};


int main() {
    Solution solution;

    // typedef std::vector<int> Array;

    std::vector<int> cases = {
        123
    };

    std::vector<int> ans = {
        321
    };

    assert(cases.size() == ans.size() && "Cases and ans sets size should be matched!");

    for(int i = 0; i < cases.size(); i++) {
        const auto res = solution.reverse(cases[i]);
        if( res != ans[i]) {
            std::cout << "Case [";
            std::cout << cases[i];
            std::cout << "] failed, expected " << ans[i] << ", got " <<  res << "\n";
            throw "Test failed\n";
        }
    }
}