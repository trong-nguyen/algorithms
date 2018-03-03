#include <iostream>
#include <tuple>
#include <unordered_map>
#include <vector>
#include <cmath>
#include <iostream>
#include <cassert>

class Solution2 {
public:
    std::vector<int> constructRectangle(int area) {
        int x = sqrt(area) + 1;
        while (area % --x == 0);
        return std::vector<int>({area / x, x});
    }
};

typedef std::tuple<int, int> Key;
struct KeyHash: public std::unary_function<Key, std::size_t>
{
    std::size_t operator()(const Key & k) const
    {
        return std::get<0>(k) ^ std::get<1>(k);
    }
};
typedef std::unordered_map<Key, int, KeyHash> Map;

class Solution {
    /*
    Given an array of scores that are non-negative integers. Player 1 picks one of the numbers from either end of the array followed by the player 2 and then player 1 and so on. Each time a player picks a number, that number will not be available for the next player. This continues until all the scores have been chosen. The player with the maximum score wins.

    Given an array of scores, predict whether player 1 is the winner. You can assume each player plays to maximize his score.

    Example 1:
    Input: [1, 5, 2]
    Output: False
    Explanation: Initially, player 1 can choose between 1 and 2.
    If he chooses 2 (or 1), then player 2 can choose from 1 (or 2) and 5. If player 2 chooses 5, then player 1 will be left with 1 (or 2).
    So, final score of player 1 is 1 + 2 = 3, and player 2 is 5.
    Hence, player 1 will never be the winner and you need to return False.
    Example 2:
    Input: [1, 5, 233, 7]
    Output: True
    Explanation: Player 1 first chooses 1. Then player 2 have to choose between 5 and 7. No matter which number player 2 choose, player 1 can choose 233.
    Finally, player 1 has more score (234) than player 2 (12), so you need to return True representing player1 can win.
    Note:
    1 <= length of the array <= 20.
    Any scores in the given array are non-negative integers and will not exceed 10,000,000.
    If the scores of both players are equal, then player 1 is still the winner.

    MinMax algorithm at its simplest form
    It's all about thinking and abstracts

    Try to answer in this form
    - I can choose either head or tail
    - If I choose:
        + head: "what is the worst outcome" (min operation)
        + tail: "what is the worst outcome"
    - Return the "least worst" (max operation) between the two

    It's best if we take an example and work from there
    i.e. [1 5 2]

    easy, player 1 not gonna win

    what if [3 1 5 2]: yes, he's gonna win, how do you know? If I select 3 then player 2 encounter
    the problem [1 5 2], and I know he will lose, so I win. If I select 2, then player 2 has to solve
    the problem [3 1 5], he can win this sub problem. BUT, who cares, I am not gonna choose 2 cause I
    already have a sure win solution by selecting 3.

    Now you see the optimal sub-structure: A[i, j] = maxop(minop(A[i+1, j]), minop(A[i, j-1]))
    Here the maxop is simply max operation
    While the minop is, thinking about it, after player 1 choose 3, we must answer what is the worst outcome (for player 1)
    if player 2 plays [1 5 2]? This is simply equivalent to "what is the best outcome (for player 2) if he plays that sub problem (first))
    Luckily we solved it before so lets use its solution (3) and remember that this is the best outcome for player 2 (though he lost in that subproblem).
    In that case what the result for player 1? Cause in this simple case we can just subtract that by the total score and then we have:
    At step (i, j)
        - player 1 select i
            the worst outcome for player 1  = total score - the best outcome for player 2 for problem(i+1, j)
                the best outcome for player 2 for problem(i+1, j) is: [
                    --- recursion ---
                    + player 2 select i+1: go find the best outcome for player 1 in (i+2, j)
                    + player 2 select j: go find the best outcome for player 1 in (i+1, j-1)
                    --- recursion ---
                ]
        - player 1 select j
            the worst outcome for player 1  = total score - the best outcome for player 2 for problem(i, j+1)
        And we just can choose the best one between choosing i and j
                    --- recursion ---
                    --- recursion ---


    */
public:
    int maxScore(const std::vector<int> & nums, int i, int j, int total, Map & lookup) const {
        Key k = Key(i, j);
        if(lookup.find(k) != lookup.end()) {
            return lookup[k];
        }

        int mx = 0;
        if(i == j - 1) {
            mx = std::max(nums[i], nums[j]); // will take the larger one
        }

        else {
            int take_i = total - maxScore(nums, i + 1, j, total - nums[i], lookup);
            int take_j = total - maxScore(nums, i, j - 1, total - nums[j], lookup);
            mx = std::max(take_i, take_j);
        }

        lookup[k] = mx; // cache it
        return mx;
    }

    bool PredictTheWinner(const std::vector<int>& nums) const {
        if(nums.size() <= 1) {
            return true;
        }

        int totalScore = 0;
        for(int i = 0; i < nums.size(); i++) {
            totalScore += nums[i];
        }

        Map lookup;
        int p1MaxScore = maxScore(nums, 0, nums.size() - 1, totalScore, lookup);

        return p1MaxScore * 2 >= totalScore; // be careful with the integer division
    }
};

typedef std::vector<int> Array;

struct AnswerSet {
    Array problem;
    bool answer;

    AnswerSet(const Array & p, bool a) {
        problem = p;
        answer = a;
    }
};

int main() {
    auto solution = Solution();

    for(const auto & as: std::vector<AnswerSet> ({
        AnswerSet(Array({0}), true)
        , AnswerSet(Array({1, 3, 1}), false)
        , AnswerSet(Array({5, 233, 7}), false)
        , AnswerSet(Array({1, 5, 233, 7}), true)
        , AnswerSet(Array({2, 4, 55, 6, 8}), false)
    })) {
        auto res = solution.PredictTheWinner(as.problem);
        // std::cout << "Result " << res << ", ans " << as.answer;
        assert(res == as.answer);
    }
}