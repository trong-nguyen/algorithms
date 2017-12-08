def is_palindrome(x):
    if x < 10:
        return True

    s = str(x)
    return s == s[::-1]

def difference(x, y):
    return abs(x - y)


def _closest_palindrome(x, palindromes, visited):
    if x < 0 or x in visited:
        return

    visited.add(x)

    if x <= 10:
        palindromes.add(x-1)
        return

    # print 'visit', x

    s = str(x)
    n = len(s)
    k = n/2

    for i in range(k):
        if s[-i-1] == s[i]:
            continue

        units = 10 ** i
        left = int(s[i]) - int(s[-i-1])
        x_left = x + left * units

        # print '\tleft', left, x_left
        if is_palindrome(x_left):
            palindromes.add(x_left)
        else:
            _closest_palindrome(x_left, palindromes, visited)

        right = 10 - abs(left)
        if left > 0:
            right = -right
        x_right = x + right * units

        # print '\tright', right, x_right
        if is_palindrome(x_right):
            palindromes.add(x_right)
        else:
            _closest_palindrome(x_right, palindromes, visited)

def closest_palindrome(x):
    if x <= 10:
        return x-1

    palindromes = set()
    visited = set()

    if is_palindrome(x):
        _closest_palindrome(x-1, palindromes, visited)
        _closest_palindrome(x+1, palindromes, visited)
    else:
        _closest_palindrome(x, palindromes, visited)

    if x in palindromes:
        palindromes.remove(x)

    lengths = map(lambda p: (difference(x,p), p), palindromes)

    # print 'found {} palindromes in {} visited'.format(len(palindromes), len(visited))
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
        (99199, 9),
        (10, 9),
        (12, 11),
        (19, 22),
        (15, 11),
        (807045053224792883, 0)
        # (19997, 20002),
        # (29999, 30003),
        # (69999, 69996),
        # (49999, 49994),
        # (38746587, 0),
        # (98769026938745, 0),
        # (19994999, 0),
        # (298736498723874659, 298736498894637892),
        # (299376498723874459, 298736498894637892),
    ]:

        result = closest_palindrome(number)
        print number, result
        # assert result == answer, 'Expected result {} for number {}'.format(answer, number)


if __name__ == '__main__':
    test()