import unittest
import random
from queues import SimpleQueue
from queues import PriorityQueue

class SimpleQueueUnitTests(unittest.TestCase):
    """
    Unit testing for a SimpleQueue object.
    """
    def setUp(self):
        self.sq = SimpleQueue()

    def test_queue_initializes_empty(self):
        """
        Does the queue initialize empty?
        """
        self.assertTrue(self.sq.is_empty())

    def test_queue_enqueues_and_dequeues_in_order(self):
        """
        Do nodes loaded into the queue get entered and removed in the correct
            order (LIFO)?
        """
        self.sq.enqueue(1)
        self.sq.enqueue(2)
        self.sq.enqueue(3)
        self.assertEqual(self.sq.dequeue(), 1)
        self.assertEqual(self.sq.dequeue(), 2)
        self.assertEqual(self.sq.dequeue(), 3)

    def test_queue_size_increments(self):
        """
        Does the variable 'size' increment when enqueuing occurs?
        """
        self.sq.enqueue('a')
        self.assertEqual(self.sq.size, 1)
        self.sq.enqueue('b')
        self.assertEqual(self.sq.size, 2)
        self.sq.enqueue('c')
        self.assertEqual(self.sq.size, 3)

    def test_queue_size_decrements(self):
        """
        Does the variable 'size' increment when enqueuing occurs?
        """
        self.sq.enqueue('a')
        self.sq.enqueue('b')
        self.sq.enqueue('c')
        self.sq.dequeue()
        self.assertEqual(self.sq.size, 2)
        self.sq.dequeue()
        self.assertEqual(self.sq.size, 1)
        self.sq.dequeue()
        self.assertEqual(self.sq.size, 0)
        # Dequeue the empty queue twice to ensure size does not become
        # negative
        self.sq.dequeue()
        self.assertEqual(self.sq.size, 0)

    def test_queue_is_not_empty(self):
        """
        Does the queue correctly report itself as not being empty when filled?
        """
        self.sq.enqueue('a')
        self.sq.enqueue('b')
        self.sq.enqueue('c')
        self.assertFalse(self.sq.is_empty())

    def test_queue_returns_to_empty(self):
        """
        After being filled and emptied, does the queue correctly report itself
            as being empty?
        """
        self.sq.enqueue('a')
        self.sq.enqueue('b')
        self.sq.enqueue('c')
        self.sq.dequeue()
        self.sq.dequeue()
        self.sq.dequeue()
        self.assertTrue(self.sq.is_empty())

class PriorityQueueUnitTests(unittest.TestCase):
    """
    Unit testing for a PriorityQueue object.
    """
    def setUp(self):
        self.pq = PriorityQueue()

    def test_queue_initializes_empty(self):
        """
        Does the queue indicate it's empty when initialized?
        """
        self.assertTrue(self.pq.is_empty())

    def test_queue_cannot_accept_uncomparables(self):
        """
        Does the queue give an error when a non-comparable type is given?
        """
        test_dict = {'a': 1}

        with self.assertRaises(TypeError):
            self.pq.add(test_dict)

    def test_queue_cannot_accept_different_types(self):
        """
        Does the queue give an error when two different types are added?
        """
        test_item_1 = 123
        test_item_2 = 'test'

        with self.assertRaises(TypeError):
            self.pq.add(test_item_1)
            self.pq.add(test_item_2)

    def test_queue_cannot_remove_from_empty(self):
        """
        Does the queue give an error when remove() is done on an empty
            queue?
        """
        with self.assertRaises(IndexError):
            self.pq.remove()

    def test_queue_cannot_heapify_empty(self):
        """
        Does the queue give an error when heapify() is done on an empty
            queue?
        """
        with self.assertRaises(IndexError):
            self.pq.heapify(0)

    def test_queue_is_not_empty(self):
        """
        Does the queue correctly report itself as not being empty when filled?
        """
        self.pq.add('a')
        self.pq.add('b')
        self.pq.add('c')
        self.assertFalse(self.pq.is_empty())

    def test_queue_returns_to_empty(self):
        """
        After being filled and emptied, does the queue correctly report itself
            as being empty?
        """
        self.pq.add('a')
        self.pq.add('b')
        self.pq.add('c')
        self.pq.remove()
        self.pq.remove()
        self.pq.remove()
        self.assertTrue(self.pq.is_empty())

    def test_queue_enqueues_and_dequeues_in_order_ints(self):
        """
        Do nodes loaded into the queue get entered and removed in the correct
            order (min heap, lowest first)? - INTEGERS
        """
        self.pq.add(510)
        self.pq.add(12)
        self.pq.add(5)
        self.pq.add(1337)
        self.pq.add(10)
        self.pq.add(1)
        self.assertEqual(self.pq.remove(), 1)
        self.assertEqual(self.pq.remove(), 5)
        self.assertEqual(self.pq.remove(), 10)
        self.assertEqual(self.pq.remove(), 12)
        self.assertEqual(self.pq.remove(), 510)
        self.assertEqual(self.pq.remove(), 1337)

    def test_queue_enqueues_and_dequeues_in_order_tuples(self):
        """
        Do nodes loaded into the queue get entered and removed in the correct
            order (min heap, lowest first)? - TUPLES
        """
        self.pq.add((10, 5))
        self.pq.add((1, 200))
        self.pq.add((502, 1))
        self.pq.add((325, 5))
        self.pq.add((8, 1234))
        self.pq.add((8, 0))
        self.assertEqual(self.pq.remove(), (1, 200))
        self.assertEqual(self.pq.remove(), (8, 0))
        self.assertEqual(self.pq.remove(), (8, 1234))
        self.assertEqual(self.pq.remove(), (10, 5))
        self.assertEqual(self.pq.remove(), (325, 5))
        self.assertEqual(self.pq.remove(), (502, 1))

    def test_queue_enqueues_and_dequeues_in_order_lists(self):
        """
        Do nodes loaded into the queue get entered and removed in the correct
            order (min heap, lowest first)? - LISTS
        """
        self.pq.add([100, 2, 3, 4, 5])
        self.pq.add([6, 7, 2, 3])
        self.pq.add([6, 7, 2, 3, 9])
        self.pq.add([1377, 78, 20, 5, 32, 8, 2])
        self.pq.add([1])
        self.pq.add([0, 1, 2])
        self.assertEqual(self.pq.remove(), [0, 1, 2])
        self.assertEqual(self.pq.remove(), [1])
        self.assertEqual(self.pq.remove(), [6, 7, 2, 3])
        self.assertEqual(self.pq.remove(), [6, 7, 2, 3, 9])
        self.assertEqual(self.pq.remove(), [100, 2, 3, 4, 5])
        self.assertEqual(self.pq.remove(), [1377, 78, 20, 5, 32, 8, 2])

    def test_queue_enqueues_and_dequeues_in_order_ints_large(self):
        """
        Do nodes loaded into the queue get entered and removed in the correct
            order (min heap, lowest first)? - INTS, LARGER SCALE
        """
        test_list = []
        for num in range(1000):
            rand_number = random.randrange(10000)
            test_list.append(rand_number)
            self.pq.add(rand_number)

        test_list.sort()
        for item in test_list:
            self.assertEqual(item, self.pq.remove())

if __name__ == '__main__':
    unittest.main()
