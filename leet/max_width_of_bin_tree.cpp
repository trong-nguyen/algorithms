#include <iostream>
#include <tuple>
#include <unordered_map>
#include <vector>
#include <cmath>
#include <iostream>
#include <cassert>


struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

#include <list>
class Solution {
public:
    typedef std::list<TreeNode *> Path;

    bool hasChildren(const TreeNode * node) {
        return node->left != NULL || node->right != NULL;
    }

    bool hasExactlyOneChild(const TreeNode * node) {
        if(node->left) {
            return node->right == NULL;
        } else if(node->right) {
            return node->left == NULL;
        } else {
            return false;
        }
    }

    bool hasBothChildren(const TreeNode * node) {
        return node->left != NULL && node->right != NULL;
    }

    bool bothNotStuck(TreeNode * leftPointer, TreeNode * rightPointer) {
        return hasChildren(leftPointer) && hasChildren(rightPointer);
    }

    bool oneStuck(TreeNode * leftPointer, TreeNode * rightPointer) {
        return hasChildren(leftPointer) || hasChildren(rightPointer);
    }

    void fastforwardUntillDiverged(Path & path) {
        TreeNode * node=0;
        // pop the path untill diverged
        while(!path.empty()) {
            node = path.pop_front();
            if(hasBothChildren(node)) {
                break;
            }
        }

        // if path empty and there is till children
        while(node && hasExactlyOneChild(node)) {
            node = (node->left ? node->left : node->right);
        }

        // node could be NULL or node must have 2 children
        // path now if not empty starts after node
        return node;
    }

    int widthOfBinaryTree(TreeNode* root) {
        if(!root) {
            return 0;
        }

        TreeNode * leftPointer = root;
        TreeNode * rightPointer = root;

        Path leftPath, rightPath;

        int maxWidth = 1;
        while(bothNotStuck(leftPointer, rightPointer)) {
            if(oneStuck(leftPointer, rightPointer)) {
                maxWidth = std::max(maxWidth, computeWidth(leftPath, rightPath));

                DivergedPoint * new_root = NULL;
                if(hasChildren(leftPointer)) {
                    rightPath.clear();
                    new_root = fastforwardUntillDiverged(leftPath);
                    if(!new_root) {
                        return maxWidth;
                    }
                    rightPath.push_back(new_root->right);

                } else {
                    leftPath.clear();
                    new_root = fastforwardUntillDiverged(rightPath);
                    if(!new_root) {
                        return maxWidth;
                    }
                    leftPath.push_back(new_root->left);
                }
            }

            // now both left and right must be advanceble
            advance(leftPath, "left");
            advance(rightPath, "right");
        }
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