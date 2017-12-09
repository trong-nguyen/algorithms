class LRUCache(object):
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.keys = [-1] * capacity
        self.values = [-1] * capacity



    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        i = self.index(key)
        if i != -1:
            value = self.values.pop(i)
            self.keys.pop(i)

            self.keys.insert(0, key)
            self.values.insert(0, value)
            return value
        else:
            return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        i = self.index(key)
        if i != -1:
            pi = i
        else:
            pi = -1

        self.keys.pop(pi)
        self.values.pop(pi)


        self.keys.insert(0, key)
        self.values.insert(0, value)



    def index(self, key):
        for i, k in enumerate(self.keys):
            if k == key:
                return i

        return -1

    def str(self):
        return str(self.keys) + str(self.values)

def test():
    cache = LRUCache(2)

    cache.put(1, 1);
    cache.put(2, 2);
    print cache.str()
    assert cache.get(1) == 1, cache.str()      # returns 1
    cache.put(3, 3)    # evicts key 2
    assert cache.get(2) == -1, cache.str()       # returns -1 (not found)
    cache.put(4, 4)    # evicts key 1
    assert cache.get(1) == -1, cache.str()       # returns -1 (not found)
    assert cache.get(3) == 3, cache.str()       # returns 3
    assert cache.get(4) == 4, cache.str()       # returns 4

    # another
    cache = LRUCache(2)
    print cache.put(2, 1)
    print cache.put(2, 1)
    print cache.get(2)
    print cache.put(1, 1)
    print cache.put(4, 1)
    print cache.get(2)

    # another
    print '\n'
    cache = LRUCache(2)
    cache.put(2, 1)
    cache.put(1, 1)
    cache.put(2, 3)
    cache.put(4, 1)
    assert cache.get(1) == -1, cache.str()
    assert cache.get(2) == 3, cache.str()

if __name__ == '__main__':
    test()