#include <vector>
#include <iostream>
#include <cassert>

class Solution
{
public:
    /*
    Check whether the array nums can be made non-decreasing by at most changing
    1 item.

    Solution:
        - Traversing the array
        - If an anomoly found, i.e. a[i] < a[i-1]
            We can correct it by either:
            + raising a[i] to a[i-1]
            + lowering a[i-1] to a[i] IF a[i] >= a[i-1]
            So as to maintain the non-decreasing property

        - The formula involve items back to 2 levels before i, e.g. i-2
        hence we need to start i at 2 and deal with initial case if array length is
        less than 3
    */

    bool checkPossibility(std::vector<int>& nums) {
        bool used = false;
        const int n = nums.size();
        if(n<2) {
            return true;
        }
        int ref = nums[1];
        if(nums[1] < nums[0]) {
            used = true;
        }

        for(int i=2; i<n; ++i) {
            if(nums[i] < ref) {
                if(used) {
                    return false;
                } else {
                    used = true;
                    if(nums[i] >= nums[i-2]) {
                        ref = nums[i];
                    } else {
                        ref = nums[i-1];
                    }
                }
            } else {
                ref = nums[i];
            }
        }

        return true;
    }
};

int main() {
    Solution solution;
    typedef std::vector<int> Array;

    std::vector<Array> cases = {
        Array({0, 9, 1, 2, 3}),
        Array({3, 4, 2, 3}),
        Array({9, 0, 1, 2, 3}),
        Array({0, 1, 2, 9, 3}),
        Array({0, 1, 1, 2, 0}),
        Array({0, 1, 2, 1, 2, 1})
    };

    std::vector<bool> ans = {true, false, true, true, true, false};

    for(int i = 0; i < cases.size(); i++) {
        if(solution.checkPossibility(cases[i]) != ans[i]) {
            std::cout << "Case [";
            for(int j=0; j<cases[i].size(); j++) {
                std::cout << cases[i][j] << " ";
            }
            std::cout << "] failed, expected " << ans[i] << "\n";
            throw "Test failed\n";
        }
    }
}