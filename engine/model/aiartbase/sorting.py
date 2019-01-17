

class MaxHeap:
    """
    This max heap class represents the
    priority queue
    """
    def __init__(self):
        """
        Intialize heap
        """
        # size
        self.size = 0

        # heap
        self.heap = None

    def insert_element(self, pos):
        if (int(pos / 2) > 0) and self.heap[int(pos / 2)] < self.heap[pos]:
            self.heap[int(pos / 2)], self.heap[pos] = self.heap[pos], self.heap[int(pos / 2)]
            self.insert_element(int(pos / 2))

    def push(self, x):
        """
        Insert x into heap
        :param x: Value to insert
        """
        self.size += 1
        if self.heap is None:
            self.heap = [None, x]
        else:
            self.heap.append(x)
            self.insert_element(self.size)

    def remove_element(self, pos):
        # caso base, pos is leaf
        element = self.heap[pos]
        while 2 * pos <= self.size:
            child = 2 * pos
            if child != self.size and self.heap[child] < self.heap[child + 1]:
                child += 1
            if element < self.heap[child]:
                self.heap[pos] = self.heap[child]
            else:
                break
            pos = child
        self.heap[pos] = element

    def pop(self):
        """
        Removes element on the top
        """
        if self.empty():
            raise Exception('Heap is empty')
        self.heap[1] = self.heap[self.size]
        self.size -= 1
        self.remove_element(1)
        self.heap.pop(self.size + 1)

    def empty(self):
        return self.size == 0

    def top(self):
        """
        Top element
        :return: max element
        """
        if self.empty():
            raise Exception('Heap is empty')

        return self.heap[1]
