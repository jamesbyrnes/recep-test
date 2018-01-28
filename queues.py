class SimpleQueue:
    """
    NOTE - This class is not currently used but is maintained here for
        posterity and for potential future use.

    A class representing a simple queue, i.e. a doubly linked list with the
    ability to enqueue (add item to the end) and dequeue (remove item from
    the front)

    Private variables are:
        head - the first SimpleQueueNode in the queue. Returns None if queue
            is empty.
        tail - the last SimpleQueueNode in the queue. Returns None if the queue
            is empty.

    Public variables are:
        size - the number of items in the queue.
    """
    def __init__(self):
        """
        Constructor for a completely empty queue.
        """
        self._head = None
        self._tail = None
        self.size = 0

    def enqueue(self, value):
        """
        Add an item to the end of the queue. Creates a new SimpleQueueNode
            to accomplish this.

        Arguments:
        value - the value of the item to be added to the end of the queue.
        """
        new_node = SimpleQueueNode(value, self._tail, None)
        if self.is_empty():
            self._head = new_node
        else:
            self._tail.next_node = new_node
        self._tail = new_node
        self.size += 1

    def dequeue(self):
        """
        Remove an item from the front of the queue. Returns None if the
            queue is empty.

        Returns:
        (any type) - the value contained in the SimpleQueueNode.
        """
        if self.is_empty():
            return None
        old_node = self._head
        self._head = old_node.next_node
        # If the head becomes empty, we're out of nodes - the tail needs to
        # be made empty, as well.
        if self._head is None:
            self._tail = None
        self.size -= 1
        return old_node.value

    def is_empty(self):
        """
        Returns a boolean indicating whether or not this queue is empty.

        Returns:
        boolean - indicating that the queue is empty or not
        """
        return self._head is None and self._tail is None

class SimpleQueueNode:
    """
    NOTE - This class is not currently used but is maintained here for
        posterity and for potential future use.

    A class representing an item in a SimpleQueue.

    Public variables are:
        prev_node - the node before this node in the queue.
        next_node - the node after this node in the queue.
        value - the item contained by the node.
    """
    def __init__(self, value, prev_node, next_node):
        """
        Constructor method.

        Arguments:
            prev_node - the node before this node in the queue.
            next_node - the node after this node in the queue.
            value - the item contained by the node.
        """
        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node

class PriorityQueue:
    """
    A class representing a min-heap priority queue, i.e. where items are
        entered onto a list and the lowest value of those items remains at the
        head of the queue.

    Public variables are:
        size - The number of items in the queue.

    Private variables are:
        _type - The type of items being added to the queue. Determined
            when the first item is added, and is maintained when the last
            item is removed.
        _nodes - The priority queue, ordered by the add() and heapify()
            methods. Organized like a binary heap.
    """
    def __init__(self):
        """
        Constructor method - returns a completely empty queue.
        """
        self._nodes = []
        self._type = None
        self.size = 0

    def is_empty(self):
        """
        Identifies whether or not the queue is empty.

        Returns:
            boolean - Whether or not self.size == 0
        """
        return self.size == 0

    def add(self, value):
        """
        Adds a value to the end of the priority queue, then "works"
            up the queue until the value's  parent's value is less than its
            value.  In this case, the value's parent is always idx/2 where idx
            is the current index of the added value.

        Arguments:
            value - A comparable value to be added. Will throw a TypeError if
                the value is not comparable (i.e. does not have methods
                __lt__, __gt__ or __eq__), or, if the queue is populated,
                when the type of the value being added and the values already
                in the queue don't match.
        """
        if self._type is not None and self._type is not type(value):
            raise TypeError('Expected type {:s} but received ' \
                    '{:s}'.format(self._type.__name__, type(value).__name__))

        # As mentioned above, we will compare the value being added to itself
        # to ensure that it can be compared to other values.
        if value.__lt__(value) is NotImplemented or \
                value.__gt__(value) is NotImplemented or \
                value.__eq__(value) is NotImplemented:
            raise TypeError('Type added to queue is not a comparable type.')

        self._nodes.append(value)
        self.size += 1

        # heap_crawler starts at the end of the queue and works up the parents
        # on the heap until the parent is <= the value added
        heap_crawler = self.size - 1

        while heap_crawler > 0 and self._nodes[int(heap_crawler / 2)] > value:
            self._nodes[heap_crawler] = self._nodes[int(heap_crawler / 2)]
            heap_crawler = int(heap_crawler / 2)

        # Insert the new value in this spot.
        self._nodes[heap_crawler] = value

    def remove(self):
        """
        Removes and returns the first value from the queue, then runs heapify()
            to re-sort the queue.

        Returns:
            (value) - The value of the first item in the queue.
        """
        if self.is_empty():
            raise IndexError("Tried to remove a value from an empty queue")

        first_item = self._nodes[0]

        # Take the last item in the queue and put it at the front,
        # then remove it from the back (no duplication). Then, reduce the size
        # of the queue.
        self._nodes[0] = self._nodes[self.size - 1]
        self._nodes.pop()
        self.size -= 1

        if self.size > 1:
            self.heapify(0)

        return first_item

    def heapify(self, root):
        """
        Re-sorts the queue starting from the root specified and down the heap,
            sorting in a heap fashion along the way. Checks the value of
            the roots children, i.e. idx * 2 + 1 and idx * 2 + 2 where idx
            is the index of the parent in the queue.

        Arguments:
            root: The starting point (as a place on the array) of the heapify
                operation.
        """
        # Drop out immediately if the root argument is out of range
        if root > self.size - 1:
            raise IndexError("Root argument given exceeds the " \
                    "size of the queue")

        moving_node = self._nodes[root]
        child_node = root
        heap_crawler = root

        # heap_crawler will now go DOWN the tree, and child_node will examine
        # its child nodes to reorder the heap

        while 2 * heap_crawler < self.size:
            child_node = 2 * heap_crawler
            if child_node < self.size - 1 and self._nodes[child_node] > self._nodes[child_node + 1]:
                # Check both children
                child_node += 1
            if moving_node <= self._nodes[child_node]:
                break
            else:
                # Continue down the tree if we haven't found a spot to place
                # the moving_node.
                self._nodes[heap_crawler] = self._nodes[child_node]
                heap_crawler = child_node
        self._nodes[heap_crawler] = moving_node
