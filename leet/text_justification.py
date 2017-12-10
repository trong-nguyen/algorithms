"""
Given an array of words and a length L, format the text such that each line has exactly L characters and is fully (left and right) justified.

You should pack your words in a greedy approach; that is, pack as many words as you can in each line. Pad extra spaces ' ' when necessary so that each line has exactly L characters.

Extra spaces between words should be distributed as evenly as possible. If the number of spaces on a line do not divide evenly between words, the empty slots on the left will be assigned more spaces than the slots on the right.

For the last line of text, it should be left justified and no extra space is inserted between words.

For example,
words: ["This", "is", "an", "example", "of", "text", "justification."]
L: 16.

Return the formatted lines as:
[
   "This    is    an",
   "example  of text",
   "justification.  "
]
Note: Each word is guaranteed not to exceed L in length.
"""

def full_justify(words, width):
    buckets = divide(words, width)
    return map(lambda w: add_paddings(w, width), buckets)

def divide(words, width):
    buckets = []
    line = []
    remained_space = width
    for word in words:
        if len(word) < remained_space:
            remained_space -= len(word) + 1 # 1 for padding
            line.append(word)
        else:
            buckets.append(line)
            line = [word]
            remained_space = width - len(word)
    if line:
        buckets.append(line)
    return buckets


def add_paddings(words, width):
    return ' '.join(words)

class Solution(object):
    def fullJustify(self, words, maxWidth):
        """
        :type words: List[str]
        :type maxWidth: int
        :rtype: List[str]
        """
        return full_justify(words, maxWidth)

def test():
    sol = Solution()
    words = ["This", "is", "an", "example", "of", "text", "justification."]
    width = 16
    res = sol.fullJustify(words, width)
    ans = [
       "This    is    an",
       "example  of text",
       "justification.  "
    ]
    print res
    # assert res == ans, res

if __name__ == '__main__':
    test()