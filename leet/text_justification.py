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
    if len(words) == 1 and not words[0]:
        return [" " * width]

    buckets = divide(words, width)
    print buckets
    first_lines = map(lambda w: add_paddings(w, width), buckets[:-1])
    last_line = ' '.join(buckets[-1])
    last_line += ' ' * (width - len(last_line))
    return first_lines + [last_line]

def divide(words, width):
    buckets = []
    line = []
    remained_space = width
    for word in words:
        if len(word) == remained_space == width:
            buckets.append([word])

        elif len(word) < remained_space:
            remained_space -= len(word) + bool(line)# 1 for padding
            line.append(word)
        else:
            buckets.append(line)
            line = [word]
            remained_space = width - len(word)
    if line:
        buckets.append(line)
    return buckets


def add_paddings(words, width):
    spaces = width - sum(map(len, words))
    if len(words) == 1:
        return words[0] + ' ' * spaces

    n = len(words) - 1
    even = spaces / n
    uneven = spaces % n
    slots = [' ' * even] * n
    if uneven > 0:
        slots[:uneven] = map(lambda x: x+' ', slots[:uneven])

    res = words[0] + ''.join(map(lambda x: x[0] + x[1], zip(slots, words[1:])))

    return res

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
    for words, width, ans in [
        (["This", "is", "an", "example", "of", "text", "justification."], 16, [
               "This    is    an",
               "example  of text",
               "justification.  "
            ]),
        (["a"], 1, ["a"]),
        ([""], 2, ["  "]),
        (["What","must","be","shall","be."], 12, ["What must be","shall be.   "]),
        (["Here","is","an","example","of","text","justification."], 14, ["Here   is   an","example     of","text          ","justification."])
    ]:
        res = sol.fullJustify(words, width)
        print res
        assert res == ans, res

if __name__ == '__main__':
    test()