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
    typedef std::list<TreeNode *> NodeList;

    int widthOfBinaryTree(TreeNode* root) {
        // let's reuse the value since it has no role in this algorithm
        if(!root) {
            return 0;
        }

        NodeList currentLevelNodes;
        root->val = 0;
        currentLevelNodes.push_back(root);
        int maxWidth = 1;
        while(!currentLevelNodes.empty()) {
            NodeList nextLevelNodes;
            for(auto node: currentLevelNodes) {
                if(node->left) {
                    nextLevelNodes.push_back(node->left);
                    node->left->val = node->val * 2;
                }
                if(node->right) {
                    nextLevelNodes.push_back(node->right);
                    node->right->val = node->val * 2 + 1;
                }
            }

            if(!nextLevelNodes.empty()) {
                maxWidth = std::max(maxWidth, nextLevelNodes.back()->val - nextLevelNodes.front()->val + 1);
            }

            currentLevelNodes = nextLevelNodes;
        }

        return maxWidth;
    }
};

#include <memory>
#include "gtest/gtest.h"

namespace {
    typedef TreeNode * Problem;
    typedef int Answer;

    class AnswerSet {
    public:
        Problem problem;
        Answer answer;

        AnswerSet(Problem & p, const Answer & a) {
            problem = p;
            answer = a;
        }
    };

    class WidthOfBinaryTreeTest: public ::testing::Test {
    protected:
        Solution solution;
        std::vector<TreeNode> nodeVault;
        int nodesUsed;

        virtual void SetUp() {
            solution = Solution();
            nodeVault.resize(1000, TreeNode(0));
            nodesUsed = 0;
        }

        TreeNode * getOneNode() {
            if(nodesUsed < nodeVault.size()) {
                return &nodeVault[nodesUsed++];
            }

            throw "All nodes used up. Increase nodeVault size.\n";
        }

        virtual ~WidthOfBinaryTreeTest() {}
    };

    TEST_F(WidthOfBinaryTreeTest, TestWidth1) {
        TreeNode * root = getOneNode();
        root->left = getOneNode();
        root->right = getOneNode();
        root->left->left = getOneNode();
        root->left->right = getOneNode();
        root->right->right = getOneNode();

        AnswerSet as(root, 4);

        ASSERT_EQ(solution.widthOfBinaryTree(as.problem), as.answer);
    }

    TEST_F(WidthOfBinaryTreeTest, TestWidth2) {
        TreeNode * root = getOneNode();
        root->left = getOneNode();
        root->left->left = getOneNode();
        root->left->right = getOneNode();

        AnswerSet as(root, 2);

        ASSERT_EQ(solution.widthOfBinaryTree(as.problem), as.answer);
    }


    TEST_F(WidthOfBinaryTreeTest, TestWidth3) {
        TreeNode * root = getOneNode();
        root->left = getOneNode();
        root->right = getOneNode();
        root->left->left = getOneNode();

        AnswerSet as(root, 2);

        ASSERT_EQ(solution.widthOfBinaryTree(as.problem), as.answer);
    }


    TEST_F(WidthOfBinaryTreeTest, TestWidth4) {
        TreeNode * root = getOneNode();
        root->left = getOneNode();
        root->left->left = getOneNode();
        root->left->left->left = getOneNode();

        root->right = getOneNode();
        root->right->right = getOneNode();
        root->right->right->right = getOneNode();

        AnswerSet as(root, 8);

        ASSERT_EQ(solution.widthOfBinaryTree(as.problem), as.answer);
    }
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

// g++ -std=c++11 -Iutils/include/ -Lutils/lib/ max_width_of_bin_tree.cpp -lgtest && ./a.out