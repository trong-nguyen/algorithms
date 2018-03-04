#include <iostream>
#include <tuple>
#include <unordered_map>
#include <vector>
#include <cmath>
#include <iostream>
#include <cassert>


typedef std::vector<int> Array;
typedef std::vector<Array> Arrays;

class Solution {
public:
    Arrays imageSmoother(const Arrays & M) {
        const int m = M.size();
        const int n = M.front().size();

        Arrays output(m, Array(n));

        for(int i = 0; i < m; i++) {
            for(int j = 0; j < n; j++) {
                int sum = 0;
                int count = 0;
                for(int u = i-1; u <= i+1; u++) {
                    for(int v = j-1; v <= j+1; v++) {
                        // ignore out-of-bound
                        if(u < 0 || u >= m || v < 0 || v >= n) {
                            continue;
                        }
                        sum += M[u][v];
                        count++;
                    }
                }
                output[i][j] = int(1. * sum / count); // count will not be 0 for any case
            }
        }

        return output;
    }
};


#include "gtest/gtest.h"

namespace {
    struct AnswerSet {
        Arrays problem;
        Arrays answer;

        AnswerSet(const Arrays & p, const Arrays & a) {
            problem = p;
            answer = a;
        }
    };

    class ImageSmootherTest: public ::testing::Test {
    protected:
        Solution solution;

        virtual void SetUp() {
            solution = Solution();
        }

        virtual ~ImageSmootherTest() {}
    };

    TEST_F(ImageSmootherTest, TestSmoothing) {
        for(const auto & as: std::vector<AnswerSet> ({
            AnswerSet(
                Arrays({
                    Array({1, 1, 1}),
                    Array({1, 0, 1}),
                    Array({1, 1, 1})
                }),
                Arrays({
                    Array({0, 0, 0}),
                    Array({0, 0, 0}),
                    Array({0, 0, 0})
                })
            )
        })) {
            auto res = solution.imageSmoother(as.problem);
            ASSERT_EQ(res, as.answer);
        }
    }
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

// g++ -std=c++11 -Iutils/include/ -Lutils/lib/ contest_46.cpp -lgtest && ./a.out