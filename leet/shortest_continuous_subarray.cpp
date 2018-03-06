#include <iostream>
#include <vector>
#include <cmath>
#include <iostream>
#include <cassert>
#include <tuple>

typedef std::vector<int> Array;
typedef std::tuple<int, int> Bound;

int bisect(const Array & a, const int v, const int i, const int j, const bool selectLeftBound) {
    /*
    Output conforms to Python bisect section
    If v is not in a, it return the index i where a[j < i] < a
    If v is in, it return the left most v if selectLeft and rightmost v + 1 if select right
    Consult tests for more examples.
    */
    if(a.empty()) {
        return 0;
    }

    int left = i;
    int right = j;

    while(left < right - 1) {
        int mid = left + (right - left) / 2;
        if(v > a[mid]) {
            left = mid;
        } else if (v < a[mid]) {
            right = mid;

        // equality case v = a[mid]
        // case           [ o mid o ]
        // seek left:  -> [ o  ]  o   : reduce right bound
        // seek right: ->   o  [  o ] : reduce left bound
        } else if(selectLeftBound) {
            right = mid;
        } else {
            left = mid;
        }
    }

    // at the end, the left bound must be right before the right bound
    // which means 1 element
    // 3 cases,
    // for when v is not equal to the current single element, call it e:
    //  - if e < v -> right, if e > v -> left
    // else if e == v, return left or right depending on the type
    if(v > a[left]) {
        return right;
    } else if(v < a[left]) {
        return left;
    } else {
        return selectLeftBound ? left : right;
    }
}

int bisectLeft(const Array & a, const int v, const int i=0, const int j=-1) {
    return bisect(a, v, i, j == -1 ? a.size() : j, true);
}

int bisectRight(const Array & a, const int v, const int i=0, const int j=-1) {
    return bisect(a, v, i, j == -1 ? a.size() : j, false);
}

class Solution {
public:
    Bound findIdealBound(const Array & a) const {
        const int n = a.size();

        int left = 0, right = n;

        while(left < n - 1 && a[left + 1] >= a[left]) {
            left++;
        }

        while(right > left + 1 && a[right - 2] <= a[right - 1]) {
            right--;
        }

        return Bound(left, right);
    }

    Bound adjustIdealBound(const Array & a, const Bound & idealBound) const {
        auto left = std::get<0>(idealBound), right = std::get<1>(idealBound);
        const int n = a.size();

        if(left >= right - 1) {
            return idealBound;
        }

        auto adjustedLeft = left;
        for(int i = left; i < right; i++) {
            if(a[i] >= a[adjustedLeft]) {
                continue;
            }

            if(a[i] < a[0]) {
                adjustedLeft = 0;
                break;
            }

            adjustedLeft = bisectRight(a, a[i], 0, adjustedLeft + 1);
        }

        auto adjustedRight = right;
        for(int i = right - 1; i >= left; i--) {
            if(a[i] <= a[adjustedRight]) {
                continue;
            }

            if(a[i] > a[n-1]) {
                adjustedRight = n;
                break;
            }

            adjustedRight = bisectLeft(a, a[i], adjustedRight, n);
        }

        return Bound(adjustedLeft, adjustedRight);
    }

    int findUnsortedSubarray(Array & nums) {
        const int n = nums.size();

        if(n <= 1) {
            return 0;
        }

        auto bound = findIdealBound(nums);
        bound = adjustIdealBound(nums, bound);

        auto left = std::get<0>(bound), right = std::get<1>(bound);

        const int elementsToSort = right - left;

        return elementsToSort > 1 ? elementsToSort : 0;
    }
};


// #include <tuple>
// #include <unordered_map>

// /*
// A Dict-like data structure with tuples as keys
// map: O(logn)
// unordered_map: O(1)
// */

// typedef std::tuple<int, int> Key;
// struct KeyHash: public std::unary_function<Key, std::size_t>
// {
//     std::size_t operator()(const Key & k) const
//     {
//         return std::get<0>(k) ^ std::get<1>(k);
//     }
// };
// typedef std::unordered_map<Key, int, KeyHash> Map;

#include "gtest/gtest.h"

namespace {
    typedef std::vector<int> Array;

    struct AnswerSetForUnitTest {
        // Define problem types here
        typedef Array Problem;
        typedef Bound Answer;

        Problem problem;
        Answer answer;

        AnswerSetForUnitTest(const Problem & p, const Answer & a) {
            problem = p;
            answer = a;
        }
    };

    struct AnswerSetForBisectTest {
        // Define problem types here
        struct Problem {
            Array array;
            int value;

            Problem(const Array & a, const int v) {
                array = a;
                value = v;
            }
        };

        typedef int Answer;

        Problem problem;
        Answer answer;

        AnswerSetForBisectTest(const Problem & p, const Answer & a):
            problem(p), answer(a) {}
    };

    class SolutionTest: public ::testing::Test {
    protected:
        Solution solution;

        virtual void SetUp() {
            solution = Solution();
        }

        // tear-down
        virtual ~SolutionTest() {

        }
    };

    TEST_F(SolutionTest, IdealBoundTest) {
        typedef AnswerSetForUnitTest AnswerSet;

        for(const auto & as: std::vector<AnswerSet> ({
            AnswerSet(Array({}), AnswerSet::Answer(0, 0))
            , AnswerSet(Array({0}), AnswerSet::Answer(0, 1))
            , AnswerSet(Array({0, 1}), AnswerSet::Answer(1, 2))
            , AnswerSet(Array({1, 0}), AnswerSet::Answer(0, 2))
            , AnswerSet(Array({0, 1, 3, 2, 4, 5}), AnswerSet::Answer(2, 4))
            , AnswerSet(Array({1, 4, 6, 5, 4, 8, 9, 4, 8, 11, 12}), AnswerSet::Answer(2, 8))
        })) {
            auto ans = solution.findIdealBound(as.problem);
            ASSERT_EQ(ans, as.answer);
        }
    }

    TEST_F(SolutionTest, BisectTestLeft) {
        typedef AnswerSetForBisectTest AnswerSet;

        for(const auto & as: std::vector<AnswerSet> ({
            AnswerSet(AnswerSet::Problem(Array({}), 3), 0)
            , AnswerSet(AnswerSet::Problem(Array({0}), 3), 1)
            , AnswerSet(AnswerSet::Problem(Array({0, 1}), 3), 2)
            , AnswerSet(AnswerSet::Problem(Array({1, 3}), 3), 1)
            , AnswerSet(AnswerSet::Problem(Array({0, 1, 2, 2, 4, 6}), 2), 2)
        })) {
            auto ans = bisectLeft(as.problem.array, as.problem.value);
            ASSERT_EQ(ans, as.answer);
        }
    }

    TEST_F(SolutionTest, BisectTestRight) {
        typedef AnswerSetForBisectTest AnswerSet;

        for(const auto & as: std::vector<AnswerSet> ({
            AnswerSet(AnswerSet::Problem(Array({}), 3), 0)
            , AnswerSet(AnswerSet::Problem(Array({0}), 3), 1)
            , AnswerSet(AnswerSet::Problem(Array({0, 1}), 3), 2)
            , AnswerSet(AnswerSet::Problem(Array({1, 3}), 3), 2)
            , AnswerSet(AnswerSet::Problem(Array({0, 1, 2, 2, 4, 6}), 2), 4)
        })) {
            auto ans = bisectRight(as.problem.array, as.problem.value);
            ASSERT_EQ(ans, as.answer);
        }
    }


    struct AnswerSetForMainTest {
        // Define problem types here
        typedef Array Problem;
        typedef int Answer;

        Problem problem;
        Answer answer;

        AnswerSetForMainTest(const Problem & p, const Answer & a) {
            problem = p;
            answer = a;
        }
    };

    TEST_F(SolutionTest, MainTest) {
        typedef AnswerSetForMainTest AnswerSet; // reuseable cause the structures are identical

        for(auto & as: std::vector<AnswerSet> ({
            AnswerSet(Array({}), 0)
            , AnswerSet(Array({0}), 0)
            , AnswerSet(Array({0, 1}), 0)
            , AnswerSet(Array({1, 0}), 2)
            , AnswerSet(Array({0, 1, 3, 2, 4, 5}), 2)
            , AnswerSet(Array({1, 4, 6, 5, 4, 8, 9, 4, 8, 11, 12}), 7)
            , AnswerSet(Array({2, 6, 4, 8, 10, 9, 15}), 5)
            , AnswerSet(Array({1, 3, 2, 2, 2}), 4)
        })) {
            auto ans = solution.findUnsortedSubarray(as.problem);
            ASSERT_EQ(ans, as.answer);
        }
    }
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

// g++ -std=c++11 -Iutils/include/ -Lutils/lib/ shortest_continuous_subarray.cpp -lgtest && ./a.out