class Solution(object):
    def _minCostClimbingStairs(self, cost, idx, mem=None):
        """
        :type cost: List[int]
        :rtype: int
        """
        if idx > len(cost) - 2:
            mem[idx] = 0
            return

        if idx == len(cost) - 2:
            mem[idx] = min(cost[-1], cost[-2])
            return

        for take in [idx+1, idx+2]:
            if take not in mem:
                self._minCostClimbingStairs(cost, take, mem)


        mem[idx] = min(cost[idx] + mem[idx+1], cost[idx+1] + mem[idx+2])

    def minCostClimbingStairs(self, cost):
        mem = {}
        self._minCostClimbingStairs(cost, 0, mem)
        return mem[0]

def test():
    solution = Solution()
    assert solution.minCostClimbingStairs([0,1,2,2]) == 2
    assert solution.minCostClimbingStairs([10, 15, 20]) == 15
    assert solution.minCostClimbingStairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) == 6


if __name__ == '__main__':
    test()