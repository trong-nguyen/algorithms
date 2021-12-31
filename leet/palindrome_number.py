class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            '''
            Negative numbers are not palindromes due to the 
            unsymmetric sign
            '''
            return False
        elif x < 10:
            '''
            Single digit numbers are palindrome
            '''
            return True
        elif x < 1e10:
            '''
            First approach to convert to string
            '''
            s = str(x)

            n = len(s)
            nh = (n // 2) if n % 2 == 0 else (n // 2 + 1)

            return s[:nh] == s[-1:-1-nh:-1]

        
        'Find all digits that make up x'
        digits = []
        remainder = x
        while True:
            digits.append(remainder % 10)
            remainder = remainder // 10
            if remainder == 0:
                break
                
        for i in range(len(digits) // 2):
            if digits[i] != digits[-1-i]:
                return False
            
        return True
            
            
            
if __name__ == '__main__':
    s = Solution()
    assert s.isPalindrome(10) == False
    assert s.isPalindrome(3) == True    
    assert s.isPalindrome(-828) == False
    assert s.isPalindrome(8222228) == True
    assert s.isPalindrome(8221228) == True