#include <vector>
#include <iostream>
#include <cassert>


void print_array(const std::vector<int>& array) {
    std::cout << "[";
    for(int i=0; i<array.size(); i++) {
        std::cout << array[i] << " ";
    }
    std::cout << "]";
}

class Solution
{
public:
    /*
    */

    void rotate(std::vector<int>& nums, int k) const {
        k = k % nums.size();

        if(k == 0) {
            return;
        }

        int start = 0;
        int cut = nums.size() - k;
        int end = nums.size();

        while(start < end - 1 and cut < end) {
            // print_array(nums);
            // std::cout << "\n";
            // std::cout << "\t" << start << " " << cut << " " << end << "\n";
            rotate_helper(nums, start, cut, end);
        }
    }

    void rotate_helper(std::vector<int>& nums, int& start, int& cut, int& end) const {
        const int n = end - start;
        const int k = end - cut;

        if(2*k >= n) {
            swap(nums, start, n - k);
            start = cut;
            cut += (n - k);
        } else {
            swap(nums, end - 2 * k, k);
            end = cut;
            cut = cut - k;
        }
    }

    void swap(std::vector<int>& nums, int start, int k) const {
        // swap k items starting from 'start' with k items starting from 'start + k'
        // std::cout << start << " " << k << " " << nums.size() << "\n";
        // assert(start + 2 * k - 1 < nums.size() && "Swapping overflow\n");

        for(int i = 0; i < k; i++) {
            const int j = start + k + i;
            const int tmp = nums[start + i];
            nums[start + i] = nums[j];
            nums[j] = tmp;
        }
    }
};

class CaseAndAnswer
{
    public:
        std::vector<int> array;
        int k;
        std::vector<int> answer;

        CaseAndAnswer(const std::vector<int>& a, int k, const std::vector<int>& ans) {
            array = a;
            this->k = k;
            answer = ans;
        }
};




int main() {
    Solution solution;
    typedef std::vector<CaseAndAnswer> Cases;
    typedef std::vector<int> Array;

    Cases cases = Cases({
        CaseAndAnswer(
            Array({1, 2}), 3,
            Array({2, 1})
        ),
        CaseAndAnswer(
            Array({1, 2, 3, 4, 5, 6}), 2,
            Array({5, 6, 1, 2, 3, 4})
        ),
        CaseAndAnswer(
            Array({1, 2}), 0,
            Array({1, 2})
        ),
        CaseAndAnswer(
            Array({1, 2}), 2,
            Array({1, 2})
        ),
        CaseAndAnswer(
            Array({0, 1}), 1,
            Array({1, 0})
        ),
        CaseAndAnswer(
            Array({0}), 1,
            Array({0})
        ),
        CaseAndAnswer(
            Array({0, 1, 2, 3, 4, 5, 6, 7}), 3,
            Array({5, 6, 7, 0, 1, 2, 3, 4})
        )
    });

    for(int i = 0; i < cases.size(); i++) {
        CaseAndAnswer& case_i  = cases[i];
        Array& array  = case_i.array;
        const int k         = case_i.k;
        const Array& answer = case_i.answer;

        solution.rotate(array, k);
        const Array& res = array;
        if(res != answer) {
            std::cout << "Case ";
            print_array(res);
            std::cout << "\nExpected";
            print_array(answer);
        } else {
            print_array(res);
            std::cout << " passed\n";
        }
    }
}