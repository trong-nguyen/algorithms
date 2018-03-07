#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>

void printF(int i, int x) {
    std::cout << "The " << i << "-th fibinaci number is " << x << "\n";
}

void printFibonaci(const int n) {
    const int f1 = 1;
    const int f2 = 1;

    printf(f1);
    printf(f2);

    int i = 3;
    while(i < n) {
        int f = f1 + f2;
        printF(i, f);

        f1 = f2
        f2 = f;
        i++;
    }
}

"aaebccaaa"
"a2e1b1c2a3"

std::string compressString(const std::string & originalString) {
    const int n = originalString.size();
    if(n < 2) {
        return originalString;
    }

    std::string compressedString;
    char c = originalString[0];
    int count = 1;
    for(int i = 1; i < n; i++) {
        if(string[i] == c && i < n - 1) {
            count++;
        } else if(i == n - 1) {
            if(string[i] == c) {
                compressedString += c + toString(count++);
            } else {
                compressedString += c + toString(count);
                compressedString += string[i] + toString(1);
            }
        }
        else {
            compressedString += c + toString(count);
            count = 1;
            c = string[i]
        }
    }

    if(compressedString.size() >= n) {
        return originalString;
    }

    return compressedString;
}




void mastermindGame(const std::string & solution, const std::string & guessString) {
    const int red(0), green(0), blue(0), yellow(0);
    const int redGuessed(0), greenGuessed(0), blueGuessed(0), yellowGuessed(0);

    int hits = 0;
    for(int i = 0; i < 4; i++) {
        if(solution[i] == guessString[i]) {
            hits++;
            continue;
        }

        if(solution[i] == "R") {
            red++;
        } else if(solution[i] == "G") {
            green++;
        } else if(solution[i] == "B") {
            blue++;
        } else if(solution[i] == "Y") {
            yellow++;
        }


        if(guessString[i] == "R") {
            redGuessed++;
        } else if(guessString[i] == "G") {
            greenGuessed++;
        } else if(guessString[i] == "B") {
            blueGuessed++;
        } else if(guessString[i] == "Y") {
            yellowGuessed++;
        }
    }


    for(int i = 0; i < 4; i++) {
        if(guessString[i] == "R") {
            redGuessed++;
        } else if(guessString[i] == "G") {
            greenGuessed++;
        } else if(guessString[i] == "B") {
            blueGuessed++;
        } else if(guessString[i] == "Y") {
            yellowGuessed++;
        }
    }

    int pseudoHits = 0;

    pseudoHits += std::min(red, redGuessed);
    pseudoHits += std::min(green, greenGuessed);
    pseudoHits += std::min(yellow, yellowGuessed);
    pseudoHits += std::min(blue, blueGuessed);

    std::cout << ""
}











int main(int argc, char** argv) {

}



1
1
2
3
5
8












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

// g++ -std=c++11 -Iutils/include/ -Lutils/lib/ trial.cpp -lgtest && ./a.out