"""
A password is considered strong if below conditions are all met:

It has at least 6 characters and at most 20 characters.
It must contain at least one lowercase letter, at least one uppercase letter, and at least one digit.
It must NOT contain three repeating characters in a row ("...aaa..." is weak, but "...aa...a..." is strong, assuming other conditions are met).
Write a function strongPasswordChecker(s), that takes a string s as input, and return the MINIMUM change required to make s a strong password. If s is already strong, return 0.

Insertion, deletion or replace of any one character are all considered as one change.

Solution:
"""

def password_check(s):
    n = len(s)

    if not 6 < n <= 20:
        return [n-20, 6-n][n<6]

    changes = 0

    return changes

class Solution(object):
    def strongPasswordChecker(self, s):
        """
        :type s: str
        :rtype: int
        """
        pass

from utils import fail_string

def test():
    solution = Solution()

    for case, ans in [
        ('StrongPass0', 0),
        ('week',)
    ]:
        res = solution.strongPasswordChecker(case)
        assert res == ans, fail_string(res, ans)

if __name__ == '__main__':
    test()