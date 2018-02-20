/*

A C++ implementation of finding the possible input arrays of a BinarySearchTree
without duplicates.

The purpose is to brush up C++ skills and test GoogleTest framework.

So far so good, the UnitTests run well and elegantly!

*/

#include <vector>
#include <iostream>

typedef int Value;
typedef std::vector<Value> Array;
typedef std::vector<Array> Arrays;

void print_array(const Array & array, int start) {
    std::cout << "[";
    for(int i = start; i < array.size(); i++) {
        std::cout << array[i];
        if(i < array.size() - 1) {
            std::cout << ",";
        }
    }
    std::cout << "]\n";
}

class Node {
public:
    Value value;
    Node * left;
    Node * right;

    Node(const Value & value) {
        this->value = value;
        left = 0;
        right = 0;
    }
};

void insert_head(Arrays & arrays, const Value & v) {
    if(arrays.empty()) {
        arrays.assign(1, Array({v}));
    } else {
        for(Arrays::iterator r = arrays.begin(); r != arrays.end(); r++) {
            r->insert(r->begin(), v);
        }
    }
}

void weave(const Array & a, int i, const Array & b, int j, Arrays & results) {
    // weave together array a starting at index i
    // and array b starting at index j
    // and store all results into the array of arrays "results"

    // this loop is just to avoid repetitive code that either advance by a or b
    for(auto x: std::vector<const Array *>{&a, &b}) {
        int ii, jj;
        if(x == &a) {
            ii = i;
            jj = j;
        } else {
            ii = j;
            jj = i;
        }
        auto y = (x == &a ? &b : &a);

        if(ii < x->size()) {
            if(jj >= y->size()) {
                results.push_back(Array(x->begin() + ii, x->end()));
            } else {
                Arrays subsequence_arrays;
                weave(*x, ii + 1, *y, jj, subsequence_arrays);
                insert_head(subsequence_arrays, x->at(ii));
                std::copy(subsequence_arrays.begin(), subsequence_arrays.end(), std::back_inserter(results));
            }
        }
    }
}

Arrays inorder_arrays(const Node * root) {
    if(!root) {
        return Arrays();
    }

    Arrays left = inorder_arrays(root->left);
    Arrays right = inorder_arrays(root->right);
    if(left.empty()) {
        insert_head(right, root->value);
        return right;
    }
    else if(right.empty()) {
        insert_head(left, root->value);
        return left;
    } else {
        Arrays results;
        for(Arrays::const_iterator li = left.begin(); li != left.end(); li++) {
            for(Arrays::const_iterator ri = right.begin(); ri != right.end(); ri++) {
                Arrays weaved;
                weave(*li, 0, *ri, 0, weaved);
                insert_head(weaved, root->value);
                std::copy(weaved.begin(), weaved.end(), std::back_inserter(results));
            }
        }
        return results;
    }
}


#include "gtest/gtest.h"

namespace {
    class InorderArrayTest: public ::testing::Test {
    protected:
        std::vector<Node> tree_nodes;
        Node * tree_root;

        InorderArrayTest() {
            tree_root = 0;
        }

        virtual void SetUp() {
            for(int i = 0; i < 10; i++){
                tree_nodes.push_back(Node(i));
            }

            tree_root = &tree_nodes[4];
            tree_root->right = &tree_nodes[5];
            tree_root->right->right = &tree_nodes[6];

            tree_root->left = &tree_nodes[1];
            tree_root->left->left = &tree_nodes[0];
            tree_root->left->right = &tree_nodes[2];
            tree_root->left->right->right = &tree_nodes[3];
        }

        virtual void TearDown() {

        }

        virtual ~InorderArrayTest() {}
    };

    class FailedInorderArrayTest: public InorderArrayTest {
    protected:
        virtual void SetUp() {
            InorderArrayTest::SetUp();
            tree_root->right->right->right = &tree_nodes[7];
            tree_root->right->right->right->right = &tree_nodes[8];
            tree_root->right->right->right->right->right = &tree_nodes[9];
        }

    };



    TEST_F(InorderArrayTest, TestTreeStructure) {
        ASSERT_EQ(tree_root->value, 4) << "Root value must be 4";
        ASSERT_EQ(tree_root->right->value, 5) << "Node value must be 5";
        ASSERT_EQ(tree_root->right->right->value, 6) << "Node value must be 6";
        ASSERT_TRUE(tree_root->right->right->left == 0) << "Node must be null";
        ASSERT_TRUE(tree_root->right->right->right == 0) << "Node must be null";

        ASSERT_EQ(tree_root->left->value, 1) << "Node value must be 1";
        ASSERT_EQ(tree_root->left->left->value, 0) << "Node value must be 0";
        ASSERT_EQ(tree_root->left->right->value, 2) << "Node value must be 2";
        ASSERT_EQ(tree_root->left->right->right->value, 3) << "Node value must be 3";

        ASSERT_TRUE(tree_root->left->left->left == 0) << "Node must be null";
        ASSERT_TRUE(tree_root->left->left->right == 0) << "Node must be null";
        ASSERT_TRUE(tree_root->left->right->right->left == 0) << "Node value must be null";
        ASSERT_TRUE(tree_root->left->right->right->right == 0) << "Node value must be null";
    }

    TEST_F(InorderArrayTest, TestPossibleInorderArrays) {
        Arrays ans = {
            Array({4, 1, 0, 2, 3, 5, 6}),
            Array({4, 1, 0, 2, 5, 6, 3}),
            Array({4, 1, 0, 2, 5, 3, 6}),
            Array({4, 1, 0, 5, 6, 2, 3}),
            Array({4, 1, 0, 5, 2, 3, 6}),
            Array({4, 1, 0, 5, 2, 6, 3}),
            Array({4, 1, 5, 6, 0, 2, 3}),
            Array({4, 1, 5, 0, 2, 3, 6}),
            Array({4, 1, 5, 0, 2, 6, 3}),
            Array({4, 1, 5, 0, 6, 2, 3}),
            Array({4, 5, 6, 1, 0, 2, 3}),
            Array({4, 5, 1, 0, 2, 3, 6}),
            Array({4, 5, 1, 0, 2, 6, 3}),
            Array({4, 5, 1, 0, 6, 2, 3}),
            Array({4, 5, 1, 6, 0, 2, 3}),
            Array({4, 1, 2, 3, 0, 5, 6}),
            Array({4, 1, 2, 3, 5, 6, 0}),
            Array({4, 1, 2, 3, 5, 0, 6}),
            Array({4, 1, 2, 5, 6, 3, 0}),
            Array({4, 1, 2, 5, 3, 0, 6}),
            Array({4, 1, 2, 5, 3, 6, 0}),
            Array({4, 1, 5, 6, 2, 3, 0}),
            Array({4, 1, 5, 2, 3, 0, 6}),
            Array({4, 1, 5, 2, 3, 6, 0}),
            Array({4, 1, 5, 2, 6, 3, 0}),
            Array({4, 5, 6, 1, 2, 3, 0}),
            Array({4, 5, 1, 2, 3, 0, 6}),
            Array({4, 5, 1, 2, 3, 6, 0}),
            Array({4, 5, 1, 2, 6, 3, 0}),
            Array({4, 5, 1, 6, 2, 3, 0}),
            Array({4, 1, 2, 0, 3, 5, 6}),
            Array({4, 1, 2, 0, 5, 6, 3}),
            Array({4, 1, 2, 0, 5, 3, 6}),
            Array({4, 1, 2, 5, 6, 0, 3}),
            Array({4, 1, 2, 5, 0, 3, 6}),
            Array({4, 1, 2, 5, 0, 6, 3}),
            Array({4, 1, 5, 6, 2, 0, 3}),
            Array({4, 1, 5, 2, 0, 3, 6}),
            Array({4, 1, 5, 2, 0, 6, 3}),
            Array({4, 1, 5, 2, 6, 0, 3}),
            Array({4, 5, 6, 1, 2, 0, 3}),
            Array({4, 5, 1, 2, 0, 3, 6}),
            Array({4, 5, 1, 2, 0, 6, 3}),
            Array({4, 5, 1, 2, 6, 0, 3}),
            Array({4, 5, 1, 6, 2, 0, 3})
        };

        Arrays res = inorder_arrays(this->tree_root);

        std::sort(res.begin(), res.end());
        std::sort(ans.begin(), ans.end());
        ASSERT_EQ(res, ans);
    }

    TEST_F(FailedInorderArrayTest, TestPossibleInorderArrays) {
        Arrays ans = {
            Array({4, 1, 0, 2, 3, 5, 6}),
            Array({4, 1, 0, 2, 5, 6, 3}),
            Array({4, 1, 0, 2, 5, 3, 6}),
            Array({4, 1, 0, 5, 6, 2, 3}),
            Array({4, 1, 0, 5, 2, 3, 6}),
            Array({4, 1, 0, 5, 2, 6, 3}),
            Array({4, 1, 5, 6, 0, 2, 3}),
            Array({4, 1, 5, 0, 2, 3, 6}),
            Array({4, 1, 5, 0, 2, 6, 3}),
            Array({4, 1, 5, 0, 6, 2, 3}),
            Array({4, 5, 6, 1, 0, 2, 3}),
            Array({4, 5, 1, 0, 2, 3, 6}),
            Array({4, 5, 1, 0, 2, 6, 3}),
            Array({4, 5, 1, 0, 6, 2, 3}),
            Array({4, 5, 1, 6, 0, 2, 3}),
            Array({4, 1, 2, 3, 0, 5, 6}),
            Array({4, 1, 2, 3, 5, 6, 0}),
            Array({4, 1, 2, 3, 5, 0, 6}),
            Array({4, 1, 2, 5, 6, 3, 0}),
            Array({4, 1, 2, 5, 3, 0, 6}),
            Array({4, 1, 2, 5, 3, 6, 0}),
            Array({4, 1, 5, 6, 2, 3, 0}),
            Array({4, 1, 5, 2, 3, 0, 6}),
            Array({4, 1, 5, 2, 3, 6, 0}),
            Array({4, 1, 5, 2, 6, 3, 0}),
            Array({4, 5, 6, 1, 2, 3, 0}),
            Array({4, 5, 1, 2, 3, 0, 6}),
            Array({4, 5, 1, 2, 3, 6, 0}),
            Array({4, 5, 1, 2, 6, 3, 0}),
            Array({4, 5, 1, 6, 2, 3, 0}),
            Array({4, 1, 2, 0, 3, 5, 6}),
            Array({4, 1, 2, 0, 5, 6, 3}),
            Array({4, 1, 2, 0, 5, 3, 6}),
            Array({4, 1, 2, 5, 6, 0, 3}),
            Array({4, 1, 2, 5, 0, 3, 6}),
            Array({4, 1, 2, 5, 0, 6, 3}),
            Array({4, 1, 5, 6, 2, 0, 3}),
            Array({4, 1, 5, 2, 0, 3, 6}),
            Array({4, 1, 5, 2, 0, 6, 3}),
            Array({4, 1, 5, 2, 6, 0, 3}),
            Array({4, 5, 6, 1, 2, 0, 3}),
            Array({4, 5, 1, 2, 0, 3, 6}),
            Array({4, 5, 1, 2, 0, 6, 3}),
            Array({4, 5, 1, 2, 6, 0, 3}),
            Array({4, 5, 1, 6, 2, 0, 3})
        };


        Arrays res = inorder_arrays(this->tree_root);
        ASSERT_EQ(res.size(), 378) << "The number of possible arrays for FailedInorderArrayTest should be 378";

        std::sort(res.begin(), res.end());
        std::sort(ans.begin(), ans.end());
        ASSERT_NE(res, ans);
    }

    TEST(ArrayWeavingTest, SimpleWeaving) {
        Array a = {1};
        Array b = {2};

        Arrays res;
        weave(a, 0, b, 0, res);

        Arrays ans = {
            Array({1, 2}),
            Array({2, 1})
        };

        // sorting to eliminate relative order difference between arrays
        std::sort(res.begin(), res.end());
        std::sort(ans.begin(), ans.end());
        ASSERT_EQ(res, ans);
    }

    TEST(ArrayWeavingTest, SimpleWeaving2) {
        Array a = {1, 3, 5};
        Array b = {2, 4};

        Arrays res;
        weave(a, 0, b, 0, res);

        Arrays ans = {
            Array({1, 3, 5, 2, 4}),
            Array({1, 3, 2, 4, 5}),
            Array({1, 3, 2, 5, 4}),
            Array({1, 2, 4, 3, 5}),
            Array({1, 2, 3, 5, 4}),
            Array({1, 2, 3, 4, 5}),
            Array({2, 4, 1, 3, 5}),
            Array({2, 1, 3, 5, 4}),
            Array({2, 1, 3, 4, 5}),
            Array({2, 1, 4, 3, 5})
        };

        std::sort(res.begin(), res.end());
        std::sort(ans.begin(), ans.end());
        ASSERT_EQ(res, ans);
    }
}

int main(int argc, char** argv) {
    // store all to-be-used nodes in a vector to cleanly manage their memory usage

    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}