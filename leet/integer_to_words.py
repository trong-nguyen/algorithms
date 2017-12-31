#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert a non-negative integer to its english words representation. Given input is guaranteed to be less than 231 - 1.

For example,
123 -> "One Hundred Twenty Three"
12345 -> "Twelve Thousand Three Hundred Forty Five"
1234567 -> "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
"""

def hundreds(num):
    unit_lookup = [
        '',
        'One',
        'Two',
        'Three',
        'Four',
        'Five',
        'Six',
        'Seven',
        'Eight',
        'Nine',
        'Ten',
        'Eleven',
        'Twelve',
        'Thirteen',
        'Fourteen',
        'Fifteen',
        'Sixteen',
        'Seventeen',
        'Eighteen',
        'Nineteen',
    ]
    tens_lookup = [
        'Twenty',
        'Thirty',
        'Forty',
        'Fifty',
        'Sixty',
        'Seventy',
        'Eighty',
        'Ninety',
    ]

    words = []
    if num >= 100:
        words += [unit_lookup[num/100], 'Hundred']

    tens = num % 100
    if tens >= 20:
        words.append(tens_lookup[tens/10-2])
        units = tens%10
        if units > 0:
            words.append(unit_lookup[units])
    elif tens > 0:
        words += [unit_lookup[tens]]

    return words


def int_to_words(num):
    if num == 0:
        return 'Zero'

    words = []
    if  num >= 1e9:
        digits = int(num / 1e9)
        if digits > 0:
            words += hundreds(digits) + ['Billion']
    if  num >= 1e6:
        digits = int(num / 1e6) % 1000
        if digits > 0:
            words += hundreds(digits) + ['Million']
    if num >= 1000:
        digits = num / 1000 % 1000
        if digits > 0:
            words += hundreds(digits) + ['Thousand']

    words += hundreds(num % 1000)
    return ' '.join(words)




import sys
from utils.templates import fail_string

def test():
    for case, ans in [
        ([1000], 'One Thousand'),
        ([20], 'Twenty'),
        ([0], "Zero"),
        ([100], "One Hundred"),
        ([123], "One Hundred Twenty Three"),
        ([12345], "Twelve Thousand Three Hundred Forty Five"),
        ([1234567], "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"),
    ]:
        res = int_to_words(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    test()