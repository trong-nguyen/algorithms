def is_palin(x):
    s = str(x)
    return s[:len(s)/2] == s[-1:-1-len(s)/2:-1]


def find_largest_palindrome(n):
    max_num = (10 ** n - 1) ** 2
    if is_palin(max_num):
        return max_num

    return next_lower_palindrome(max_num)

def is_valid(palindrome, n):
    palindrome = int(palindrome)
    max_num = 10 ** n - 1
    for i in range(max_num, 10 ** (n-1) - 1, -1):
        if palindrome % i == 0:
            print '\t', palindrome / i
            return True

    return False

def next_lower_palindrome(p):
    s = str(p)
    left = str(int(s[:len(s)/2]) - 1)

    return left + left[::-1] if len(s) % 2 == 0 else s[:len(s)/2+1][::-1]



def first_palindrome(n):
    palindrome = find_largest_palindrome(n)


    while palindrome > 10 ** n:
        if is_valid(palindrome, n):
            return palindrome

        palindrome = next_lower_palindrome(palindrome)
        print palindrome


if __name__ == '__main__':
    print first_palindrome(6)