#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>


#include <tuple>
#include <unordered_map>

/*
A Dict-like data structure with tuples as keys
*/

typedef std::tuple<int, int> Key;
struct KeyHash: public std::unary_function<Key, std::size_t>
{
    std::size_t operator()(const Key & k) const
    {
        return std::get<0>(k) ^ std::get<1>(k);
    }
};
typedef std::unordered_map<Key, int, KeyHash> Map;

#include "gtest/gtest.h"

namespace {
    typedef std::vector<int> Array;
    typedef Array Problem;
    typedef bool Answer;


    struct AnswerSet {
        Problem problem;
        Answer answer;

        AnswerSet(const Problem & p, const Answer & a):
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

    TEST_F(SolutionTest, UnitTest) {
        for(const auto & as: std::vector<AnswerSet> ({
            AnswerSet(Array({0}), true)
        })) {
            auto result = solution.solve(as.problem);
            ASSERT_TRUE(result == as.answer);
        }
    }
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

// g++ -std=c++11 -Iutils/include/ -Lutils/lib/ YOUR_CPP_FILE.cpp -lgtest && ./a.out