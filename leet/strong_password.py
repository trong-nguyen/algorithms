"""
A password is considered strong if below conditions are all met:

It has at least 6 characters and at most 20 characters.
It must contain at least one lowercase letter, at least one uppercase letter, and at least one digit.
It must NOT contain three repeating characters in a row ("...aaa..." is weak, but "...aa...a..." is strong, assuming other conditions are met).
Write a function strongPasswordChecker(s), that takes a string s as input, and return the MINIMUM change required to make s a strong password. If s is already strong, return 0.

Insertion, deletion or replace of any one character are all considered as one change.

Solution:
- Divide violations in to 3 categories:
    + Length
        - Negative (removals needed)
        - Positive (insertions required)
    + Character types (digit/upper/lower)
    + Repetitions

- Facts:
    - Changes to correct positive length and repetion can be utilized
        to correct character types as well
    - Negative and positive length changes have very different effects
        + Negative (removals) length changes can only be used to decrease repetitions
            (and some might remove the repetitions - when lowered to 2)
        + Positive length changes can, at the same time, correct some of the
            characters type (insert the missing characters) and repetition type
            (insert in between repetitions)


"""

DEBUG = False

import re

def check_characters(s):
    """
    requirements of 1 each for upper, lower and digit are mutually exclusive
    """
    required = [r'[A-Z]', r'[a-z]', r'\d']

    return sum(map(lambda p: re.search(p, s) == None, required))

def check_repetitions(s, length_changes):
    THRESHOLD = 3

    groups = re.findall(r'(.)(\1*)', s)

    # quarantine the original repetitions
    repetitions = map(len, map(''.join, groups))
    repetitions = filter(lambda r: r >= THRESHOLD, repetitions)

    # utilize the negative length changes (removals)
    # to incorporate repetition changes
    # negative length changes is the absolute, lower bound of changes
    changes = length_changes

    # utilize negative length changes to reduce repetition
    repetitions = sorted(repetitions, key=lambda r: r % THRESHOLD)
    while changes < 0 and repetitions:
        repetitions[0] -= 1
        changes += 1
        if repetitions[0] < THRESHOLD:
            repetitions.pop(0)

    # utilize positive length changes, insert right after (Threshold-1) repeating characters
    # to remove them from spotted repeating groups
    if changes > 0:
        repetitions = sorted(repetitions, reverse=True)
        for i, rep in enumerate(repetitions):
            repetitions[i] -= THRESHOLD - 1
            changes -= 1
            if changes == 0:
                break
        repetitions = filter(lambda r: r >= THRESHOLD, repetitions)

    changes_each_group = map(lambda x: x/THRESHOLD, repetitions)

    return sum(changes_each_group)



def check_length(s):
    n = len(s)

    if not 6 <= n <= 20:
        return [20-n, 6-n][n<6]

    return 0


def password_check(s):
    length_changes     = check_length(s)
    chars_changes      = check_characters(s)
    repetition_changes = check_repetitions(s, length_changes)

    if DEBUG:
        print 'L {}, R {}, C {}'.format(length_changes, repetition_changes, chars_changes)

    if length_changes >= 0:
        # if we need to increase length
        # characters change if required can be incorporated to that change plus the reptition change
        # i.e. add more character that satisfy the character requirement (is lower / upper / digit)
        return max(length_changes + repetition_changes, chars_changes)
    else:
        # but if we need to decrease length
        # that change is independent to the other changes
        return max(repetition_changes, chars_changes) + abs(length_changes)



class Solution(object):
    def strongPasswordChecker(self, s):
        """
        :type s: str
        :rtype: int
        """
        return password_check(s)

from utils import fail_string

def test():
    solution = Solution()

    for case, ans in [
        ("aaaaabbbb1234567890ABA", 3),
        ("aaaabbaaabbaaa123456A", 3),
        ("AAAAA", 2),
        ("...", 3),
        ("..................!!!", 7),
        ('129dK8l8jjj129dk8l8jl', 1),
        ('StrongPass0', 0),
        ('aaaa', 2),
        ('', 6),
        ('aaa', 3),
        ('aaaaaa', 2),
        ("aaa111", 2),
        ("ABABABABABABABABABAB1", 2),
        ("aaaaaaaaaaaaaaaaaaaaa", 7),
        ("1234567890123456Baaaaa", 3),
    ]:
        res = solution.strongPasswordChecker(case)
        assert res == ans, fail_string(res, ans)

if __name__ == '__main__':
    test()