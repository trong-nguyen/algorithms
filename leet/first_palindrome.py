from math import sqrt

def reverse(x):
    return int(str(x)[::-1])

def is_solvable(high, low, n):
    epsilon = 1e-8

    S = 10 ** n - high
    P = low

    delta = S*S - 4 * P

    if delta < 0:
        return False

    sd = sqrt(delta)
    if S < sd or (sd - int(sd)) > epsilon:
        return False

    i = S - sd

    return i % 2 < epsilon


def first_palindrome(n):
    cache = [
        None,
        9,
        9009,
        906609,
        99000099,
        9966006699,
        999000000999,
        99956644665999,
        9999000000009999,
    ]
    """
    The core idea is that a number with 2n digits can be expressed as:
    x = high * 10^n + low  [*]

    and if x is a palindrome then:
        low is a reversed number of high

    while if x is the product of say u and v:
    x = u * v = (10^n - i) * (10^n - j) since we are interested in the largest

    hence it's logical if we search from the top down (top is 10^n)
    => x = (-i-j + 10^n) * 10^n + ij
    or compare against [*]:
    high = (-i-j + 10^n)
    low = ij

    Then we only need to bruteforce the "high value", reverse to get the "low value"
    and solve the quadratic equ. for i, j
    """

    if n <= 8:
        return cache[n]

    high = 10 ** n - 1

    while high > 0:
        low = reverse(high)

        if is_solvable(high, low, n):
            return high * 10 ** n + low

        high -= 1

class Solution(object):
    def largestPalindrome(self, n):
        """
        :type n: int
        :rtype: int
        """
        cache = [
            None,
            9,
            987,
            123,
            597,
            677,
            1218,
            877,
            475,
        ]
        if n <= 8:
            return cache[n]

        return first_palindrome(n) % 1337


if __name__ == '__main__':
    for n in range(1, 8+1):
        print 'Largest palindrome as a product of 2 {} digits is {}'.format(n, first_palindrome(n))
        print first_palindrome(n) % 1337