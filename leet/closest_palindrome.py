"""
PROBLEM:
Given an integer n, find the closest integer (not including itself), which is a palindrome.

The 'closest' is defined as absolute difference minimized between two integers.

Example 1:
Input: "123"
Output: "121"
Note:
The input n is a positive integer represented by string, whose length will not exceed 18.
If there is a tie, return the smaller one as answer.

SOLUTION:
Facts:
    - Brute force: increase / decrease gradually to find results, O(n)
    - Flip and memoization: O(d) where d is the length of n stringified
    - We only need to flip the right half of the stringified number to converge to palindromes
    - If we start from the right most going left and match it to the left most, the flipped digits will remain unchanged
    - There are 2 ways to match digits: say t is the target and x is the current value, we either go
        x + (t-x)
        or +/-(10) + t
        Ex: target 3
            current 1
            either go +2 or -8
        depending on the index of the considered digit
            we need to add 10^i (i the digit index) to the current number
        Ex: number 1982, consider digit 8, matching to 9, we either go:
            +1 -> +1 * 10^1 + 1982 = 1992 (a palindrome)
            -9 -> -9 * 10^1 + 1982 = 1892 (not a palindrome, though it matches the previous palindrome in that index)
    - The worst case cost is O(2^d) where d is half the length of stringified n
    - With memoization it could be reduced to O(d) by not checking the repeated cases

"""
def is_palindrome(x):
    s = str(x)
    return s == s[::-1]

def difference(x, y):
    return abs(x - y)


def traverse_palindromes(x, palindromes, visited):
    """
    Flip the right-most non-matching digit of x up and down recursively
    Stop when a palindrome is reached or already visited
    Add the found palindromes to a hash table
    Add the visited numbers to another
    """
    if x < 0 or x in visited:
        return

    visited.add(x)

    if x == 10:
        palindromes.add(9)
        return
    elif is_palindrome(x):
        palindromes.add(x)
        return

    s = str(x)
    k = len(s)/2

    for i in range(k):
        if s[-i-1] == s[i]:
            continue

        left = int(s[i]) - int(s[-i-1])
        right = [10, -10][int(left > 0)] + left

        for shift in (left, right):
            x_next = x + shift * 10 ** i
            traverse_palindromes(x_next, palindromes, visited)

        break

def closest_palindrome(x):
    """
    Find the closest palindrome
    if x is already a palindrome
    pertube x minimally by +/-1 and traverse
    After searching done, return the closest-distanced palindrome (except x)
    """
    if x <= 0:
        raise Exception('non-positive numbers!')
    elif x <= 10:
        return x-1

    palindromes = set()
    visited = set()

    if is_palindrome(x):
        traverse_palindromes(x-1, palindromes, visited)
        traverse_palindromes(x+1, palindromes, visited)
        palindromes.remove(x)
    else:
        traverse_palindromes(x, palindromes, visited)

    lengths = map(lambda p: (difference(x,p), p), palindromes)

    print 'found {} palindromes in {} visited'.format(len(palindromes), len(visited))
    return min(lengths)[1]

# Leetcode solution class
class Solution(object):
    def nearestPalindromic(self, n):
        """
        :type n: str
        :rtype: str
        """
        return str(closest_palindrome(int(n)))

def test():
    for number, answer in [
        # (19999999998, 1)
        (1, 0),
        (11, 9),
        (99199, 99099),
        (10, 9),
        (12, 11),
        (19, 22),
        (15, 11),
        (807045053224792883, 807045053350540708),
        (19997, 20002),
        (29999, 30003),
        (69999, 69996),
        (49999, 49994),
        (38746587, 38744783),
        (98769026938745, 98769022096789),
        (19994999, 19999991),
        (298736498723874659, 298736498894637892),
        (299376498723874459, 299376498894673992),
        (2034509299376498723874459, 2034509299376739929054302),
        (283745238034509299376498723874459, 283745238034509303905430832547382),
        (2837452380345092993764987238744598364967, 2837452380345092993773992905430832547382),
    ]:

        result = closest_palindrome(number)
        print number, result
        assert result == answer, 'Expected result {} for number {}'.format(answer, number)


if __name__ == '__main__':
    test()