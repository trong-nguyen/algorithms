#include <iostream>
#include <tuple>
#include <unordered_map>
#include <vector>
#include <cmath>
#include <iostream>
#include <cassert>

class Solution {
public:
    std::vector<int> lexicalOrder(int n) {

    }
};

#include "gtest/gtest.h"

namespace {
    typedef std::vector<int> Array;
    struct AnswerSet {
        Array problem;
        bool answer;

        AnswerSet(const Array & p, bool a) {
            problem = p;
            answer = a;
        }
    };

    class PredictWinnerTest: public ::testing::Test {
    protected:
        Solution solution;

        virtual void SetUp() {
            solution = Solution();
        }

        virtual ~PredictWinnerTest() {}
    };

    TEST_F(PredictWinnerTest, TestPredictions) {
        for(const auto & as: std::vector<AnswerSet> ({
            AnswerSet(Array({0}), true)
            , AnswerSet(Array({1, 3, 1}), false)
            , AnswerSet(Array({5, 233, 7}), false)
            , AnswerSet(Array({1, 5, 233, 7}), true)
            , AnswerSet(Array({2, 4, 55, 6, 8}), false)
        })) {
            ASSERT_TRUE(solution.PredictTheWinner(as.problem) == as.answer);
        }
    }
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

// g++ -std=c++11 -Iutils/include/ -Lutils/lib/ virtual_contest_492.cpp -lgtest && ./a.out