#include <iostream>
#include <vector>
#include <cmath>
#include <iostream>
#include <cassert>
#include <limits>

#include <string>
#include <unordered_map>

typedef std::vector<int> Array;

class Solution {
public:
    /*
    n the video game Fallout 4, the quest "Road to Freedom" requires players to reach a metal dial called the "Freedom Trail Ring", and use the dial to spell a specific keyword in order to open the door.

    Given a string ring, which represents the code engraved on the outer ring and another string key, which represents the keyword needs to be spelled. You need to find the minimum number of steps in order to spell all the characters in the keyword.

    Initially, the first character of the ring is aligned at 12:00 direction. You need to spell all the characters in the string key one by one by rotating the ring clockwise or anticlockwise to make each character of the string key aligned at 12:00 direction and then by pressing the center button.
    At the stage of rotating the ring to spell the key character key[i]:
    You can rotate the ring clockwise or anticlockwise one place, which counts as 1 step. The final purpose of the rotation is to align one of the string ring's characters at the 12:00 direction, where this character must equal to the character key[i].
    If the character key[i] has been aligned at the 12:00 direction, you need to press the center button to spell, which also counts as 1 step. After the pressing, you could begin to spell the next character in the key (next stage), otherwise, you've finished all the spelling.
    Example:


    Input: ring = "godding", key = "gd"
    Output: 4
    Explanation:
     For the first key character 'g', since it is already in place, we just need 1 step to spell this character.
     For the second key character 'd', we need to rotate the ring "godding" anticlockwise by two steps to make it become "ddinggo".
     Also, we need 1 more step for spelling.
     So the final output is 4.
    Note:
    Length of both ring and key will be in range 1 to 100.
    There are only lowercase letters in both strings and might be some duplcate characters in both strings.
    It's guaranteed that string key could always be spelled by rotating the string ring.


    Solution:
        Tried to mathematically formulate the substructure by:
        Given a ring R and key K
        We have to find a path from K[0:n] that minimize the distance travelled

        This is a bottom up approach, dynamic programming.

        R = "abbaac"
        K = "abc"

        Assume that we arrive at the key n - 2, i.e. just before the last key: b
        There are ONLY 2 ways that we arrive at the last key c: from b0 (indexed 1) or b1 (indexed 2)
        Clearly it is the path through b1 is the shortest with distance = 2, the other is 3. Though do not hesitate to select b1
        since we have to take into account the distance from the beginning to b1 + b1 to c
        compared to the distance from the beginning to b0 and from b0 to c

        We can form a vector that represent the shortest path from a certain key to the end:

        V[c-c] (character c to the last key, which is itself) = [0]
            with dimension equal to the number  of occurence of the corresponding character (here the last one c)
        V[b-c] = [
            d[b0 to c0] + min(c0 to c),
            d[b1 to c0] + min(c0 to c),
        ]
            now you see the dimension is equal to the occurence of b in the ring

        V[a-c] = [
            min( [ d[a0 to b0] + V[b0-c], d[a0 to b1] + V[b1-c]) ] ),
            min( [ d[a1 to b0] + V[b0-c], d[a1 to b1] + V[b1-c]) ] ),
            min( [ d[a2 to b0] + V[b0-c], d[a2 to b1] + V[b1-c]) ] ),
        ]
            now the dimension is equal to the occurence of a in ring, which is 3

        Generally, the shortest paths from a key ki to the end will be equal to the shortest among:
            - The distance from it to one of the occurences of the next key (in ring R) plus the shortest path from that occurence
            to the end

        So you can see the pattern, and clearly we can work bottom up with minimal storage for the current key only.

        Cost: O(m*m*n) time, O(m) space where m is the size of the ring and n of the key
        We carry n steps iterating over key
        For each step we calculate the distances between pairs of certain occurences of k and k+1
        O(m) space is required in the mapping of the ring characteres (to quickly search for occurences)
        and the current shortest path vector, which is as many as the size of the ring (see ring="aaaaaabbbbb" and key="ab")
    */
    typedef char Key;
    typedef std::unordered_map<Key, Array> Map;

    Map mapRingChars(const std::string & ring) const {
        // map the occurences of characters in ring
        // i.e. for ring = "ccac"
        // map["c"] = [0, 1, 3] <- characters c occur at indices 0, 1 and 3
        Map ringMap;

        for(int i = 0; i < ring.size(); i++) {
            ringMap[ring[i]].push_back(i);
        }

        return ringMap;
    }

    int computeRingDistance(int i, int j, int ringSize) const {
        // compute the wrap-around distance between items at i and j

        // for performance, we "might" skip this check and trust the users
        // if(i < 0 || j < 0 || i >= ringSize || j >= ringSize) {
        //     throw "Invalid ring indices";
        // }

        auto d = abs(i - j);
        return std::min(d, ringSize - d);
    }

    int findRotateSteps(const std::string & ring, const std::string & key) {
        if(key.empty()) {
            return 0;
        }

        const auto BIG = std::numeric_limits<int>::max();

        const int ringSize = ring.size();
        auto ringMap = mapRingChars(ring);

        auto shortestDistance = Array(ringMap[key.back()].size(), 0);
        for(int i = key.size() - 2; i >= 0; i--) {
            const char k = key[i];
            const char k1 = key[i + 1];

            // skip the repetitive keys, obviously the shortest is itself
            if(k == key[i + 1]) {
                continue;
            }
            const auto & tail = ringMap[k];
            const auto & head = ringMap[k1];

            auto newShortestDistance = Array(tail.size());
            for(const auto & u: tail) {
                const auto uIndex = &u - &tail[0];
                int shortest = BIG;
                for(const auto & v: head) {
                    auto vIndex = &v - &head[0];
                    shortest = std::min(shortest, computeRingDistance(u, v, ringSize) + shortestDistance[vIndex]);
                }

                newShortestDistance[uIndex] = shortest;
            }

            shortestDistance = newShortestDistance;
        }

        auto shortestRotatingSteps = BIG;
        const auto & firstCharIndices = ringMap[key[0]];
        for(int i = 0; i < shortestDistance.size(); ++i){
            shortestRotatingSteps = std::min(
                shortestRotatingSteps,
                computeRingDistance(0, firstCharIndices[i], ringSize) + shortestDistance[i]
                );
        }

        const auto pressingSteps = key.size();

        return pressingSteps + shortestRotatingSteps;
    }
};



#include <tuple>
#include <unordered_map>

/*
A Dict-like data structure with tuples as keys
map: O(logn)
unordered_map: O(1)
*/

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
    typedef int Answer;


    struct AnswerSet {
        struct Problem {
            std::string ring;
            std::string key;

            Problem(const std::string & r, const std::string & k): ring(r), key(k) {}
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
            AnswerSet(AnswerSet::Problem("ba", "a"), 2)
            , AnswerSet(AnswerSet::Problem("godding", "gd"), 4)
            , AnswerSet(AnswerSet::Problem("ababcab", "acbaacba"), 17)
            , AnswerSet(AnswerSet::Problem("godding", "ogd"), 7)
            , AnswerSet(AnswerSet::Problem("ababcab", "acbaacba"), 17)

        })) {
            auto res = solution.findRotateSteps(as.problem.ring, as.problem.key);
            ASSERT_EQ(res, as.answer);
        }
    }
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

// g++ -std=c++11 -Iutils/include/ -Lutils/lib/ freedom_trail.cpp -lgtest && ./a.out