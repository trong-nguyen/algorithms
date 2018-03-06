#include <iostream>
#include <vector>
#include <cmath>
#include <iostream>
#include <cassert>

#include <tuple>
#include <unordered_map>

/*
A Dict-like data structure with tuples as keys
map: O(logn)
unordered_map: O(1)
*/

typedef std::tuple<int, int> Key;
struct SymmetricKeyHash: public std::unary_function<Key, std::size_t>
{
    std::size_t operator()(const Key & k) const
    {
        return std::get<0>(k) ^ std::get<1>(k);
    }
};

typedef std::unordered_map<Key, bool, SymmetricKeyHash> TupleMap;
typedef std::unordered_map<int, bool> Map;

class Solution {
public:
    int findPairs(const std::vector<int>& nums, const int k) {
        if(k < 0) {
            return 0;
        }

        TupleMap countedPairs;
        Map visited;

        for (int i = 0; i < nums.size(); ++i) {
            auto u = nums[i];
            auto v1 = u + k, v2 = u - k;

            for(auto v: std::vector<int>({u + k, u - k})) {
                if(visited.find(v) != visited.end()) {
                    auto key = Key(u, v);
                    if(countedPairs.find(Key(v, u)) == countedPairs.end()) {
                        countedPairs[key] = true;
                    }
                }
            }

            visited[u] = true;
        }

        // for(auto p: countedPairs) {
        //     std::cout << std::get<0>(p.first) << " " << std::get<1>(p.first) << "\n";
        // }
        return countedPairs.size();
    }
};



#include "gtest/gtest.h"

namespace {
    typedef std::vector<int> Array;
    typedef Array Problem;
    typedef int Answer;


    struct AnswerSet {
        struct Problem {
            Array array;
            int k;

            Problem(const Array & a, const int k): array(a), k(k) {}
        };

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
            AnswerSet(AnswerSet::Problem(Array({}), 0), 0)
            , AnswerSet(AnswerSet::Problem(Array({6,3,5,7,2,3,3,8,2,4}), 2), 5)
            , AnswerSet(AnswerSet::Problem(Array({1,1,1,2,1}), 1), 1)
            , AnswerSet(AnswerSet::Problem(Array({1,1,1,2,1}), 1), 1)
            , AnswerSet(AnswerSet::Problem(Array({1,2,3,4,5}), -1), 0)
            , AnswerSet(AnswerSet::Problem(Array({1,2,3,4,5}), 3), 2)
            , AnswerSet(AnswerSet::Problem(Array({0}), 0), 0)
            , AnswerSet(AnswerSet::Problem(Array({1, 2}), 1), 1)
            , AnswerSet(AnswerSet::Problem(Array({3, 1, 4, 1, 5}), 2), 2)
            , AnswerSet(AnswerSet::Problem(Array({1, 2, 3, 4, 5}), 1), 4)
            , AnswerSet(AnswerSet::Problem(Array({1, 3, 1, 5, 4}), 0), 1)
        })) {
            ASSERT_EQ(solution.findPairs(as.problem.array, as.problem.k), as.answer);
        }
    }
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

// printf "\033c" && g++ -std=c++11 -Iutils/include/ -Lutils/lib/ contest_22.cpp -lgtest && ./a.out