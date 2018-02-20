#include <vector>
#include <iostream>

typedef int Value;
typedef std::vector<Value> Array;
typedef std::vector<Array> Arrays;

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
        arrays.assign(1, Array(v));
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

    if(i < a.size()) {
        if(j >= b.size()) {
            results.push_back(a);
        } else {
            Arrays subsequence_arrays;
            weave(a, i + 1, b, j, subsequence_arrays);
            insert_head(subsequence_arrays, a[i]);
            std::copy(subsequence_arrays.begin(), subsequence_arrays.end(), results.end());
        }
    }

    if(j < b.size()) {
        if(i >= a.size()) {
            results.push_back(b);
        } else {
            Arrays subsequence_arrays;
            weave(a, i, b, j + 1, subsequence_arrays);
            insert_head(subsequence_arrays, b[j]);
            std::copy(subsequence_arrays.begin(), subsequence_arrays.end(), results.end());
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
        for(Arrays::iterator li = left.begin(); li != left.end(); li++) {
            for(Arrays::iterator ri = right.begin(); ri != right.end(); ri++) {
                Arrays weaved;
                weave(*li, 0, *ri, 0, weaved);
                insert_head(weaved, root->value);
                std::copy(weaved.begin(), weaved.end(), results.end());
            }
        }
        return results;
    }
}

void print_array(const Array & array) {
    std::cout << "[";
    for(int i = 0; i < array.size(); i++) {
        std::cout << array[i];
        if(i < array.size() - 1) {
            std::cout << ",";
        }
    }
    std::cout << "]\n";
}

int main(int argc, char** argv) {
    // store all to-be-used nodes in a vector to cleanly manage their memory usage
    std::vector<Node> nodes;
    for(int i = 0; i < 10; i++){
        nodes.push_back(Node(i));
    }

    Node * root = &nodes[4];
    root->right = &nodes[5];
    root->right->right = &nodes[6];

    root->left = &nodes[1];
    root->left->left = &nodes[0];
    root->left->right = &nodes[2];
    root->left->right->right = &nodes[3];

    Arrays res = inorder_arrays(root);
    for(Arrays::iterator ai = res.begin(); ai != res.end(); ai++) {
        print_array(*ai);
    }
}