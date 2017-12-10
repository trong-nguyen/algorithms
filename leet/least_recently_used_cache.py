"""
Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following operations: get and put.

get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity, it should invalidate the least recently used item before inserting a new item.

Follow up:
Could you do both operations in O(1) time complexity?

Example:

LRUCache cache = new LRUCache( 2 /* capacity */ );

cache.put(1, 1);
cache.put(2, 2);
cache.get(1);       // returns 1
cache.put(3, 3);    // evicts key 2
cache.get(2);       // returns -1 (not found)
cache.put(4, 4);    // evicts key 1
cache.get(1);       // returns -1 (not found)
cache.get(3);       // returns 3
cache.get(4);       // returns 4

Using a heap would result in:
O(k) cost for both get and put
    - get() -> O(k) to search for element and return it PLUS if the key is found: do the removepush()
        + remove it from the heap, heapify the remaining
        + push the updated to the heap again
    - put() -> O(k) to search for element,
        + if existed update and do the removepush()
        + if not pop and push the new

but then it doesn't worth using the heap since we are stuck with O(k) cost anyway

Using a LinkedHashMap:
    - Components: a HashMap H and a DoublyLinkedList L
    - H[key] = node in L
    - L has the structure of Tail-Node1-Node2-...-Head where closer to the Tail indicates less frequently used and vice versa to the Head
    - get(key) action:
        + key in H: get the node in L, bring the node to the head
        + key not in H: return none
    - put(key) action:
        + key in H: get the node in L, update priority
        + key not in H:
            * pop the rearest node
            * get the content of the node, get the key from the content
            * delete that key from H
            * pluck the node off the L
            * reinsert the node to the front

Cost: O(1) for access and insertions

Facts:
Only nodes tail node position really matters (since we need to rip it off when capacity reached)
Others are more or less equal in terms of access priority (we keep them in the map). But the less frequently they are accessed
the more they move closer to the tail, since access nodes are inserted to the head.

Data structure that:
    - Allows O(1) insertion and removals: LinkedList
    - Allow O(1) accessing: HashMap

"""

class DoublyLinkedNode(object):
    """The node in a doubly linked list"""
    def __init__(self, content):
        super(DoublyLinkedNode, self).__init__()
        self.content = content
        self.front = None
        self.rear = None

class DoublyLinkedList(object):
    """List that support front and rear connections"""
    def __init__(self):
        super(DoublyLinkedList, self).__init__()
        head = DoublyLinkedNode(None)
        tail = DoublyLinkedNode(None)
        head.rear = tail
        tail.front = head

        self.head = head
        self.tail = tail

    def pluck_off(self, node):
        """
        Remove node from the linked list
        """
        if node in [self.head, self.tail]:
            return

        # amend link
        rear_node = node.rear
        front_node = node.front

        rear_node.front = front_node
        front_node.rear = rear_node

    def insert_before(self, front_node, new_node):
        """Insert the node right before front_node"""
        nb_node = front_node.rear

        new_node.front = front_node
        front_node.rear = new_node

        new_node.rear = nb_node
        nb_node.front = new_node

    def push_front(self, node):
        """Move the existing node to the front"""
        self.pluck_off(node)
        self.insert_before(self.head, node)

    def add_front(self, node):
        """Insert the node to the front"""
        self.insert_before(self.head, node)

    def pop_rear(self):
        """Pluck off the rearest node right after the tail and return it"""
        node = self.tail.front
        if node != self.head:
            self.pluck_off(node)
            return node
        else:
            raise Exception('Trying to pop an empty list')

    def __str__(self):
        cursor = self.tail.front
        array = []
        while cursor != self.head:
            array.append(cursor.content['key'])
            cursor = cursor.front
        return '[{}]'.format(' '.join(map(str, array)))


class LRUCache(object):
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.map = {}
        self.list = DoublyLinkedList()

    def get(self, key):
        """
        get the node with key in cache
        if the key is in the cache, update its priority (bring it to the front)
        """
        if key in self.map:
            node = self.map[key]
            self.list.push_front(node)
            return node.content['value']
        else:
            return -1

    def put(self, key, value):
        """
        Insert the node to the front
        Pop off one rear node if capacity reached
        """
        if key in self.map:
            node = self.map[key]
            node.content['value'] = value
            self.list.push_front(node)
        else:
            node = DoublyLinkedNode({'key': key, 'value': value})
            if self.capacity <= len(self.map):
                removed_node = self.list.pop_rear()
                removed_key = removed_node.content['key']
                del self.map[removed_key]

            self.map[key] = node
            self.list.add_front(node)

    def __str__(self):
        return self.list.__str__()

def test():
    DEBUG = True
    cache = LRUCache(2)

    cache.put(1, 1); print cache
    cache.put(2, 2); print cache
    if DEBUG: print cache
    assert cache.get(1) == 1
    if DEBUG: print cache
    cache.put(3, 3)    # evicts key 2
    if DEBUG: print cache
    assert cache.get(2) == -1
    cache.put(4, 4)    # evicts key 1
    if DEBUG: print cache
    assert cache.get(1) == -1
    if DEBUG: print cache
    assert cache.get(3) == 3
    if DEBUG: print cache
    assert cache.get(4) == 4

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
    assert cache.get(1) == -1, cache
    assert cache.get(2) == 3, cache

if __name__ == '__main__':
    test()