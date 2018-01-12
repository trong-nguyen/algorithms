#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Say you have an array for which the ith element is the price of a given stock on day i.

Design an algorithm to find the maximum profit. You may complete at most k transactions.

Note:
You may not engage in multiple transactions at the same time (ie, you must sell the stock before you buy again).

Credits:
Special thanks to @Freezen for adding this problem and creating all test cases.
"""
import random
def derive_profitable_trades(prices):
    """
    Compute the trades that has positive profits
    a trade is defined as period where prices increase / decrease monotonically
    Consider only trades that has positive profits, return their profits
        price(i+1) > price(i) for i in a profitable (positive) trade
    """
    trades = [0]

    p_low = prices[0]
    for p in prices:
        profit = p - p_low
        if profit == 0:
            continue # flat market, takes no position

        # keep accumulating profits if the market is bullish
        if profit > 0:
            trades[-1] += profit

        # entering bearish
        else:
            if trades[-1] != 0:
                trades.append(0)

        p_low = p

    if trades[-1] == 0:
        del trades[-1]

    return trades

def swap(items, i, j):
    items[i], items[j] = items[j], items[i]

def partition(items, i, j, pivot_index):
    """
    Partition myth:
        select one index (pivot_index) and get the value at that index
        move all items less than that value to the left, not less than (equal or larger) to the right
        return the new index of that value after swaps

        Note that in this case we choose to have "equal or larger" to the right due to
        the fact that we are more interested in the "larger" part

        Let i and j running towards each other, starting from the left and right most, respectively
        i and j only stops at illegal values, values where items[i] >= pivot or items[j] < pivot
        One the positions found, we swap them and can be assured that the values come at or before i
        and at or after j now are perfectly aligned to the partition condition
        (items[x] < pivot and items[y] >= pivot where x <= i and y >= j).

        The tricky thing happens when an i is found but the j is not, which means all items[x] where x >= i
        is larger or equal to pivot. But sadly items[i] it self might be larger than pivot so it is not a valid
        resulting index.
        If that happens:
        - We need a buffer that contains the pivot value, we select the left most position i0 = original i
        and swap the values at pivot_index and i0. This is done before we do the partition.
        - And we start the partitioning at i0 + 1 to not touch that buffer value. That buffer value is guaranteed
        to be a valid pivot_index after the partition (since it is the pivot value after all)
        - Now if we run in the aforementioned situation (items[i] > pivot
        (and not equal so the final pivot_index should be before this i) but there is no j that items[j] < pivot and j >= i).
        Then we would like for j to stop right before that i, i.e. j = i - 1. This is the position that guarantees
        items[j] strictly less than pivot value but strategically before the conflict happens, i.e. before i where items[i]
        might be larger than value.
        - Now the trick really takes place, remember the buffer that contains our pivot? Just swap it with value at j.
        Since items[j] is strictly less than pivot so there is no problem if we pull it to the left without
        affects the partition property. And j is now the index of the pivot value (just swapped) where
        items[k>=j] >= pivot and items[k<j] < pivot strictly.

    """
    pivot = items[pivot_index]
    swap(items, i, pivot_index)
    i0 = i
    i += 1
    while True:
        while i < j and items[i] < pivot:
            i += 1
        while j >= i and items[j] >= pivot:
            j -= 1

        if j > i:
            swap(items, i, j)
        else:
            break
    swap(items, i0, j)
    return j




def select_k_largest_items(items, i, j, k):
    """
    """
    # print items[i:j]
    n = j - i

    if n < 1:
        return []

    if k >= n:
        return items[i:j]


    pivot_index = random.randrange(i, j)

    pivot_index = partition(items, i, j-1, pivot_index)

    m = j - pivot_index

    if k == m:
        return items[pivot_index:j]
    elif k < m:
        return select_k_largest_items(items, pivot_index+1, j, k)
    else:
        return select_k_largest_items(items, i, pivot_index, k - m) + items[pivot_index:j]


def buy_low_sell_high(prices, transactions):
    trades = derive_profitable_trades(prices)

    if transactions / 2 >= len(trades):
        return sum(trades)
    else:
        k = transactions / 2 # buy - sell pairs
        k_largest = select_k_largest_items(trades, 0, len(trades), k)
        return sum(k_largest)


class Solution(object):
    def maxProfit(self, k, prices):
        """
        :type k: int
        :type prices: List[int]
        :rtype: int
        """
        return buy_low_sell_high(prices, transactions)


import sys
from utils.templates import fail_string

def unit_test():
    array = [1, 3, 2]
    res = partition(array, 0, len(array)-1, 2)
    assert res == 1 and array == [1, 2, 3], array
    array = [2, 1, 3, 2]
    res = partition(array, 0, len(array)-1, 3)
    assert res == 1 and array == [1, 2, 3, 2], array

    array = [0, 1, 2, 3, 4]
    res = partition(array, 0, len(array)-1, 4)
    assert res == 4

    array = [0, 3, 2, 4, 1]
    res = partition(array, 0, len(array)-1, 3)
    assert res == 4

    array = [0, 0, 0, 0, 0]
    res = partition(array, 0, len(array)-1, 0)
    assert res == 0, res

    array = [0, 0, 0, 0, 0]
    res = partition(array, 0, len(array)-1, 4)
    assert res == 0

    array = [1, 0, 2, 0, 4]
    res = partition(array, 0, len(array)-1, 3)
    assert res == 0

    array = [1, 0, 2, 2, 0, 4]
    res = partition(array, 0, len(array)-1, 2)
    assert res == 3

    array = [0, 1, 2, 3, 4]
    res = select_k_largest_items(array, 0, len(array), 3)
    assert sorted(res) == [2, 3, 4], res

    array = [1, 1, 1, 1, 1, 1]
    res = select_k_largest_items(array, 0, len(array), 3)
    assert sorted(res) == [1, 1, 1]


def test():
    for case, ans in [
        ([[0, 1, -1, 1, 2, 1, 3], 2], 3),
        ([[0, 1, -1, 1, 2, 1, 3], 6], 6),
        ([[0, 1, -1, 1, 2, 1, 3], 4], 5),
    ]:
        res = buy_low_sell_high(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    unit_test()
    test()