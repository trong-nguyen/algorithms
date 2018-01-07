#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implement wildcard pattern matching with support for '.' and '*'.

'.' Matches any single character.
'*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

The function prototype should be:
bool isMatch(const char *s, const char *p)

Some examples:
isMatch("aa","a") → false
isMatch("aa","aa") → true
isMatch("aaa","aa") → false
isMatch("aa", "a*") → true
isMatch("aa", ".*") → true
isMatch("ab", ".*") → true
isMatch("aab", "c*a*b") → true

SOLUTION:
    Refer to wildcard_matching problem.
    This one differs only in that * is matched against the "preceding" element.
    So it appears to be closer to the familiar regex engines found in most libraries.
"""

import re

REGEX = {
    'START': '^',
    'END': '$',
    'ONE': '.',
    'ALL': '*',
    'TERMINAL': 'TERMINAL',
}

class AutomataMachine(object):
    """Implements the NFA - Non-deterministic Finite Automata"""

    def __init__(self, pattern):
        super(AutomataMachine, self).__init__()
        START = REGEX['START']
        END = REGEX['END']

        translators = self.translators = {}

        if not pattern:
            translators[START] = self.make_translator(REGEX['TERMINAL'], fr=START, to=END)

        pattern = self.preprocess_pattern(pattern)
        for i, description in enumerate(pattern):
            fr = START if i == 0 else i
            to = END if i == len(pattern) - 1 else i+1
            translators[fr] = self.make_translator(description, fr=fr, to=to)

        translators[END] = self.make_translator(REGEX['TERMINAL'], fr=END, to=END)

    @staticmethod
    def preprocess_pattern(pattern):
        # to avoid having to deal with multiple matchall translators
        return re.sub(r'\*{2,}', '*', pattern)


    def translate(self, char, from_states):
        next_states = map(lambda s: self.next_state(s, char), from_states)
        next_states = reduce(lambda x, y: x+y, next_states)
        return set(filter(bool, next_states))

    def next_state(self, current, char):
        return self.translators[current](char)

    @staticmethod
    def make_translator(description, fr, to):
        # return a function that returns next states (possibly multi)
        if description == REGEX['TERMINAL']:
            # the terminator translator is the one that translate the match state
            # it can only return the match state if empty char is fed
            # else it becomes void (meaning it matchs up to some point in the word)
            # but not the remaining part
            return lambda c: (to if not c else None, )
        elif description == REGEX['ONE']:
            # the any
            return lambda c: (to if c != '' else fr, )
        elif description == REGEX['ALL']:
            # the any and loop back
            return lambda c: (to, fr)
        else:
            return lambda c: (to,) if c == description else (fr,) if c == '' else (None,)

    def __str__(self):
        output = 'Translators\n'
        output += str(self.translators)
        return output

    def is_match(self, word):
        START = REGEX['START']

        states = {START}
        for char in word:
            # fast forward the current states as far as possible
            # before consuming characters
            states = self.translate(char, self.fast_forward(states))
            if not states:
                return False

        return self.can_fast_forward_to_end(states)

    def fast_forward(self, states):
        while True:
            # print 'stagnant', states, next_states
            next_states = self.translate('', states)
            new_states = next_states.difference(states)
            if not new_states:
                break
            states = states.union(new_states)
        return states

    def can_fast_forward_to_end(self, states):
        """
        see if the current states can be fast forwarded to the end state
        by feeding empty chars to it (astericks translators can still proceed)
        """
        while states:
            next_states = self.fast_forward(states)
            if REGEX['END'] in states:
                return True
            if next_states == states:
                return False
            states = next_states

        return False

def regex_is_match(s, p):
    one = REGEX['ONE']
    pattern = p
    if one != '.':
        pattern = pattern.replace(one, '.')
    # pattern = pattern.replace('*', '.*?')
    pattern += '$'
    c = re.compile(pattern)
    return c.match(s) != None

def collapse_asterisks(p):
    pattern = re.sub(r'\*{2,}', '*', p)
    return pattern

class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """

        p = collapse_asterisks(p)

        if p.count('*') < 23:
            return regex_is_match(s, p)

        return AutomataMachine(p).is_match(s)

import sys
from utils.templates import fail_string

def test():
    for case, ans in [
        # (['a' * 23, 'a.' * 23 + 'a' * 23], False),
        # (["abcde", "*.*.*.*."], True),
        # (['c', '.*'], True),
        # (['c', '*.'], True),
        # (['c', '*.*'], True),
        # (['', '.'], False),
        # (['', ''], True),
        # ([' ', ''], False),
        # (["a","a"], True),
        # (["bbbb","bbbb"], True),
        # (["askdhfpasiudyfhkjshbdkljfhiushdf","askdhfpasiudyfhkjshbdkljfhiushdf"], True),
        # (["b","."], True),
        # (["skjdfhaskjdhflkjhj","."*len('skjdfhaskjdhflkjhj')], True),
        # (["c","*"], True),
        # (["","*"], True),
        # (["kjsadhflkujhdslfkj","*"], True),
        # (['', '**'], True),
        # (['a', 'a*'], True),
        # (['zl', 'z.*'], True),
        # (['zld', 'z.*'], True),
        # (['zlahsdklfjh', 'z.*'], True),
        (["aa","a"], False),
        (["aa","aa"], True),
        (["aaa","aa"], False),
        (["aa", "a*"], True),
        (["aa", ".*"], True),
        (["ab", ".*"], True),
        (["aab", "c*a*b"], True),
#         (["aaaabaaaabbbbaabbbaabbaababbabbaaaababaaabbbbbbaabbbabababbaaabaabaaaaaabbaabbbbaababbababaabbbaababbbba", "*****b*aba***babaa*bbaba***a*aaba*b*aa**a*b**ba***a*a*"], True),
#         (["abbabaaabbabbaababbabbbbbabbbabbbabaaaaababababbbabababaabbababaabbbbbbaaaabababbbaabbbbaabbbbababababbaabbaababaabbbababababbbbaaabbbbbabaaaabbababbbbaababaabbababbbbbababbbabaaaaaaaabbbbbaabaaababaaaabb",
#             "**aa*****ba*a*bb**aa*ab****a*aaaaaa***a*aaaa**bbabb*b*b**aaaaaaaaa*a********ba*bbb***a*ba*bb*bb**a*b*bb"], False),
#         (["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
# "*aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa*"], False)
    ]:
        string, pattern = case
        solution = Solution()
        res = solution.isMatch(string, pattern)
        try:
            assert res == ans
        except AssertionError as e:
            sys.exit(fail_string(res=res, ans=ans, case=case))

if __name__ == '__main__':
    test()