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

    if transactions >= len(trades):
        return sum(trades)
    else:
        k = transactions # buy - sell pairs
        k_largest = select_k_largest_items(trades, 0, len(trades), k)
        return sum(k_largest)

def max_profit(prices, j, transactions_left, mem):
    if j < 2:
        return 0
    if transactions_left <= 0:
        return mem[()]

    pid = (transactions_left, j) # profit id
    if pid in mem:
        return mem[pid]

    # profit = 0
    # for k in range(i+1, j):
    #     # engage in a trade, buying at i
    #     p_ik = prices[k] - prices[i]
    #     if p_ik > 0:
    #         profit = max(profit, p_ik + max_profit(prices, k+1, j, transactions_left-1, mem))
    #     else:
    #         # versus hold on for a while, skip buying at i
    #         profit = max(profit, max_profit(prices, k, j, transactions_left, mem))


    # if prices[i+1] <= prices[i]:
    #     return max_profit(prices, i+1, j, transactions_left, mem)

    profit = 0
    for m in range(1, 30, 2):
        if i+m < j:
            dp = prices[i+m] - prices[i]
            if dp > 0:
                profit = max(profit, dp + max_profit(prices, i+m+1, j, transactions_left-1, mem))
                profit = max(profit, max_profit(prices, i+m+1, j, transactions_left, mem))
            else:
                break
        else:
            break

    # if (j-1, transactions) not in mem:
    #     max_profit(j-1, transactions, mem)

    # previous_profit, _ = mem[(j-1, transactions)]

    # _, previous_cost = mem[(j-1, transactions - 1)]

    # profit = max(previous_profit, prices[j-1] - previous_cost)

    # mem[(transactions, j)] = profit, max(previous_cost, prices[j-1] - profit)

    return profit

def compress_prices(prices):
    trades = [0]
    for i, p in enumerate(prices[0:-1]):
        derivative = prices[i+1] - p
        if derivative * trades[-1] < 0:
            trades.append(0)
        trades[-1] += derivative


    if trades[-1] == 0:
        del trades[-1]

    compressed = [0]
    for t in trades:
        compressed.append(compressed[-1] + t)

    return compressed


def best_buy(prices, transactions):
    # all_trades = {}
    # for i in range(len(prices)):
    #     for j in range(i+1, len(prices)):
    #         all_trades[(i, j)] = prices[j] - prices[i]

    # return 1

    trades = derive_profitable_trades(prices)
    if transactions >= len(trades):
        # if we have the ability to make micro-transactions (lots of transaction continuously)
        # the max profit will be the sum of all bullish segments
        # print 'Short-circuit'
        return sum(trades)

    # mem = {}
    # res = max_profit(prices, 0, len(prices), transactions, mem)

    mem = {}
    if len(prices) < 2:
        return 0

    for k in range(transactions):
        mem[(k, 1)] = 0

    mem[(0, 2)] = 0, 0
    dp = max(0, prices[1] - prices[0])
    for k in range(1, transactions):
        if k == 0:
            mem[(k, 2)] = 0
        mem[(k, 2)] = dp

    k = transactions - 1
    cost_1 = mem[(transactions-1, 1)] - prices[0]
    cost_2 = mem[(transactions-1, 2)] - prices[1]
    max_cost = max(cost_1, cost_2)
    print mem
    for j in range(2, len(prices)):
        profit = 0
        for k in range(1, transactions):
            previous_profit = mem[(k, j-1)]

            profit = max(profit, previous_profit, prices[j] - max_cost)
            mem[(k, j+1)] = profit
            max_cost = max(max_cost, profit - prices[j])

    return mem[(k, len(prices))]

    # res = max_profit(prices, len(prices), transactions, mem)

    # print mem
    return res



class Solution(object):
    def maxProfit(self, k, prices):
        """
        :type k: int
        :type prices: List[int]
        :rtype: int
        """
        if not prices:
            return 0

        # print prices
        prices = compress_prices(prices)
        # print '\t', prices

        # print len(prices)
        # return buy_low_sell_high(prices, k)

        return best_buy(prices, k)


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
    solution = Solution()
    for case, ans in [
        # ([29, [70,4,83,56,94,72,78,43,2,86,65,100,94,56,41,66,3,33,10,3,45,94,15,12,78,60,58,0,58,15,21,7,11,41,12,96,83,77,47,62,27,19,40,63,30,4,77,52,17,57,21,66,63,29,51,40,37,6,44,42,92,16,64,33,31,51,36,0,29,95,92,35,66,91,19,21,100,95,40,61,15,83,31,55,59,84,21,99,45,64,90,25,40,6,41,5,25,52,59,61,51,37,92,90,20,20,96,66,79,28,83,60,91,30,52,55,1,99,8,68,14,84,59,5,34,93,25,10,93,21,35,66,88,20,97,25,63,80,20,86,33,53,43,86,53,55,61,77,9,2,56,78,43,19,68,69,49,1,6,5,82,46,24,33,85,24,56,51,45,100,94,26,15,33,35,59,25,65,32,26,93,73,0,40,92,56,76,18,2,45,64,66,64,39,77,1,55,90,10,27,85,40,95,78,39,40,62,30,12,57,84,95,86,57,41,52,77,17,9,15,33,17,68,63,59,40,5,63,30,86,57,5,55,47,0,92,95,100,25,79,84,93,83,93,18,20,32,63,65,56,68,7,31,100,88,93,11,43,20,13,54,34,29,90,50,24,13,44,89,57,65,95,58,32,67,38,2,41,4,63,56,88,39,57,10,1,97,98,25,45,96,35,22,0,37,74,98,14,37,77,54,40,17,9,28,83,13,92,3,8,60,52,64,8,87,77,96,70,61,3,96,83,56,5,99,81,94,3,38,91,55,83,15,30,39,54,79,55,86,85,32,27,20,74,91,99,100,46,69,77,34,97,0,50,51,21,12,3,84,84,48,69,94,28,64,36,70,34,70,11,89,58,6,90,86,4,97,63,10,37,48,68,30,29,53,4,91,7,56,63,22,93,69,93,1,85,11,20,41,36,66,67,57,76,85,37,80,99,63,23,71,11,73,41,48,54,61,49,91,97,60,38,99,8,17,2,5,56,3,69,90,62,75,76,55,71,83,34,2,36,56,40,15,62,39,78,7,37,58,22,64,59,80,16,2,34,83,43,40,39,38,35,89,72,56,77,78,14,45,0,57,32,82,93,96,3,51,27,36,38,1,19,66,98,93,91,18,95,93,39,12,40,73,100,17,72,93,25,35,45,91,78,13,97,56,40,69,86,69,99,4,36,36,82,35,52,12,46,74,57,65,91,51,41,42,17,78,49,75,9,23,65,44,47,93,84,70,19,22,57,27,84,57,85,2,61,17,90,34,49,74,64,46,61,0,28,57,78,75,31,27,24,10,93,34,19,75,53,17,26,2,41,89,79,37,14,93,55,74,11,77,60,61,2,68,0,15,12,47,12,48,57,73,17,18,11,83,38,5,36,53,94,40,48,81,53,32,53,12,21,90,100,32,29,94,92,83,80,36,73,59,61,43,100,36,71,89,9,24,56,7,48,34,58,0,43,34,18,1,29,97,70,92,88,0,48,51,53,0,50,21,91,23,34,49,19,17,9,23,43,87,72,39,17,17,97,14,29,4,10,84,10,33,100,86,43,20,22,58,90,70,48,23,75,4,66,97,95,1,80,24,43,97,15,38,53,55,86,63,40,7,26,60,95,12,98,15,95,71,86,46,33,68,32,86,89,18,88,97,32,42,5,57,13,1,23,34,37,13,65,13,47,55,85,37,57,14,89,94,57,13,6,98,47,52,51,19,99,42,1,19,74,60,8,48,28,65,6,12,57,49,27,95,1,2,10,25,49,68,57,32,99,24,19,25,32,89,88,73,96,57,14,65,34,8,82,9,94,91,19,53,61,70,54,4,66,26,8,63,62,9,20,42,17,52,97,51,53,19,48,76,40,80,6,1,89,52,70,38,95,62,24,88,64,42,61,6,50,91,87,69,13,58,43,98,19,94,65,56,72,20,72,92,85,58,46,67,2,23,88,58,25,88,18,92,46,15,18,37,9,90,2,38,0,16,86,44,69,71,70,30,38,17,69,69,80,73,79,56,17,95,12,37,43,5,5,6,42,16,44,22,62,37,86,8,51,73,46,44,15,98,54,22,47,28,11,75,52,49,38,84,55,3,69,100,54,66,6,23,98,22,99,21,74,75,33,67,8,80,90,23,46,93,69,85,46,87,76,93,38,77,37,72,35,3,82,11,67,46,53,29,60,33,12,62,23,27,72,35,63,68,14,35,27,98,94,65,3,13,48,83,27,84,86,49,31,63,40,12,34,79,61,47,29,33,52,100,85,38,24,1,16,62,89,36,74,9,49,62,89]], 2818),
        # ([2, []], 0),
        ([2, [2,1,2,0,1]], 2),
        ([2, [0, 1, -1, 1, 2, 1, 3]], 5),
        ([3, [0, 1, -1, 1, 2, 1, 3]], 6),
        ([4, [0, 1, -1, 1, 2, 1, 3]], 6),
    ]:
        res = solution.maxProfit(*case)
        try:
            assert res == ans
        except AssertionError as e:
            status = fail_string(res=res, ans=ans, case=case)
            sys.exit(status)

if __name__ == '__main__':
    unit_test()
    test()