/*

Reverse an integer, handling overflow cases

-2^31 + 1 <= reverse(x) <= 2^31

get the digits of number and convert them from highest order to lowest
*/

#include <vector>
#include <iostream>
#include <cassert>
#include <cmath>

#define MAX_POSITIVE 2147483648
#define MAX_NEGATIVE -2147483647

int numDigits(long x) {
    // x is positive
    assert(x >= 0);

    int d = 0; // 32 bit - 1(signed)
    while(pow(10, ++d) <= x);
    return d - 1;
}

class Solution {
public:
    int reverse(long x) {
        const int sign = x >= 0 ? 1 : -1;
        x = x * sign; // make it positive
        const int d = numDigits(x);

        long reversed = 0;

        for(int i = d; i >=0; i--) {
            const long units = pow(10, i);
            int xi = x / units; // note the implitcit conversion
            reversed += xi * pow(10, d - i);
            x = x % units;
        }

        reversed *= sign;

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

    std::vector<long> cases = {
        10,
        123,
        120,
        (long)(pow(2, 30)) + 1,
        4281473701,
        -(long)(pow(2, 30)),
        -4281473701,
        -3281473701,
        12000000,
        120000021,
        -2147483412
    };

    std::vector<long> ans = {
        1,
        321,
        21,
        0,
        1073741824,
        0,
        -1073741824,
        -1073741823,
        21,
        120000021,
        -2143847412
    };

    assert(cases.size() == ans.size() && "Cases and ans sets size should be matched!");

    for(int i = 0; i < cases.size(); i++) {
        const auto res = solution.reverse(cases[i]);
        if( res != ans[i]) {
            std::cout << "Case [";
            std::cout << cases[i];
            std::cout << "] failed, expected " << ans[i] << ", got " <<  res << "\n";
            throw "Test failed\n";
        } else {
            std::cout << "case " << cases[i] << ", res " << res << " passed\n";
        }
    }
}