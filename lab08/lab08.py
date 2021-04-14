from unittest import TestCase
import random
import functools

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################


class Heap:
    def __init__(self, key=lambda x: x):
        self.data = []
        self.key = key

    @staticmethod
    def _parent(idx):
        return (idx-1)//2

    @staticmethod
    def _left(idx):
        return idx*2+1

    @staticmethod
    def _right(idx):
        return idx*2+2

    def pos_exists(self, n):
        return n < len(self)

    def switch_node(self, parent, child):
        parentval = self.data[parent]
        childval = self.data[child]
        self.data[parent] = childval
        self.data[child] = parentval

    def heapify(self, idx=0):
        # BEGIN SOLUTION
        lc = Heap._left(idx)
        rc = Heap._right(idx)
        if len(self.data) != 0:
            curval = self.key(self.data[idx])

            if self.pos_exists(lc):
                if self.pos_exists(rc):
                    lcval = self.key(self.data[lc])
                    rcval = self.key(self.data[rc])

                    if lcval > curval or rcval > curval:
                        if lcval > rcval:

                            self.switch_node(idx, lc)
                            self.heapify(lc)
                        else:

                            self.switch_node(idx, rc)
                            self.heapify(rc)
                else:
                    lcval = self.key(self.data[lc])

                    if lcval > curval:

                        self.switch_node(idx, lc)
                        self.heapify(lc)
            elif self.pos_exists(rc):
                rcval = self.key(self.data[rc])

                if rcval > curval:

                    self.switch_node(idx, rc)
                    self.heapify(rc)
        # END SOLUTION

    def trickle_up(self, idx):
        if idx > 0:
            p = Heap._parent(idx)
            pval = self.data[p]
            curval = self.data[idx]
            if self.key(pval) < self.key(curval):
                self.switch_node(p, idx)
                self.trickle_up(p)

    def add(self, x):
        # BEGIN SOLUTION
        self.data.append(x)
        self.trickle_up(len(self.data)-1)
        # END SOLUTION

    def peek(self):
        return self.data[0]

    def pop(self):
        ret = self.data[0]
        self.data[0] = self.data[len(self.data)-1]
        del self.data[len(self.data)-1]
        self.heapify()
        return ret

    def __iter__(self):
        return self.data.__iter__()

    def __bool__(self):
        return len(self.data) > 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################

# (6 point)


def test_key_heap_1():
    from unittest import TestCase
    import random

    tc = TestCase()
    h = Heap()

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [97, 61, 65, 49, 51, 53, 62, 5, 38, 33])

# (6 point)


def test_key_heap_2():
    tc = TestCase()
    h = Heap(lambda x: -x)

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [5, 33, 53, 38, 49, 65, 62, 97, 51, 61])

# (6 points)


def test_key_heap_3():
    tc = TestCase()
    h = Heap(lambda s: len(s))

    h.add('hello')
    h.add('hi')
    h.add('abracadabra')
    h.add('supercalifragilisticexpialidocious')
    h.add('0')

    tc.assertEqual(h.data,
                   ['supercalifragilisticexpialidocious', 'abracadabra', 'hello', 'hi', '0'])

# (6 points)


def test_key_heap_4():
    tc = TestCase()
    h = Heap()

    random.seed(0)
    lst = list(range(-1000, 1000))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in range(999, -1000, -1):
        tc.assertEqual(x, h.pop())

# (6 points)


def test_key_heap_5():
    tc = TestCase()
    h = Heap(key=lambda x: abs(x))

    random.seed(0)
    lst = list(range(-1000, 1000, 3))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in reversed(sorted(range(-1000, 1000, 3), key=lambda x: abs(x))):
        tc.assertEqual(x, h.pop())

################################################################################
# 2. MEDIAN
################################################################################


def running_medians(iterable):
    # BEGIN SOLUTION
    medians = []
    lower = Heap()
    higher = Heap(key=lambda x: -1*x)
    for val in iterable:
        if not higher and not lower:
            lower.add(val)
            medians.append(val)
            continue
        elif val < medians[-1]:
            if len(lower) > len(higher):
                higher.add(lower.pop())
                lower.add(val)
            elif len(lower) < len(higher):
                lower.add(val)
            else:
                lower.add(val)
        else:
            if len(lower) < len(higher):
                lower.add(higher.pop())
                higher.add(val)
            elif len(lower) > len(higher):
                higher.add(val)
            else:
                higher.add(val)

        if len(higher) == len(lower):
            medians.append((higher.peek()+lower.peek())/2)
        elif len(higher) > len(lower):
            medians.append(higher.peek())
        else:
            medians.append(lower.peek())

    return medians

    # END SOLUTION

    ################################################################################
    # TESTS
    ################################################################################


def running_medians_naive(iterable):
    values = []
    medians = []
    for i, x in enumerate(iterable):
        values.append(x)
        values.sort()
        if i % 2 == 0:
            medians.append(values[i//2])
        else:
            medians.append((values[i//2] + values[i//2+1]) / 2)
    return medians

# (13 points)


def test_median_1():
    tc = TestCase()
    tc.assertEqual([3, 2.0, 3, 6.0, 9], running_medians([3, 1, 9, 25, 12]))

# (13 points)


def test_median_2():
    tc = TestCase()
    vals = [random.randrange(10000) for _ in range(1000)]
    tc.assertEqual(running_medians_naive(vals), running_medians(vals))

# MUST COMPLETE IN UNDER 10 seconds!
# (14 points)


def test_median_3():
    tc = TestCase()
    vals = [random.randrange(100000) for _ in range(100001)]
    m_mid = sorted(vals[:50001])[50001//2]
    m_final = sorted(vals)[len(vals)//2]
    running = running_medians(vals)
    tc.assertEqual(m_mid, running[50000])
    tc.assertEqual(m_final, running[-1])

################################################################################
# 3. TOP-K
################################################################################


def topk(items, k, keyf):
    # BEGIN SOLUTION
    topk = Heap(key=lambda x: keyf(x) * -1)
    for item in items:
        if not topk:
            topk.add(item)
        elif keyf(item) > keyf(topk.peek()) and len(topk) >= k:
            topk.pop()
            topk.add(item)
        elif len(topk) < k:
            topk.add(item)

    answers = []
    while topk:
        answers.insert(0, topk.pop())

    return answers
    # END SOLUTION

    ################################################################################
    # TESTS
    ################################################################################


def get_age(s):
    return s[1]


def naive_topk(l, k, keyf):
    def revkey(x): return keyf(x) * -1
    return sorted(l, key=revkey)[0:k]

# (30 points)


def test_topk_students():
    tc = TestCase()
    students = [('Peter', 33), ('Bob', 23), ('Alice', 21), ('Gertrud', 53)]

    tc.assertEqual(naive_topk(students, 2, get_age),
                   topk(students, 2, get_age))

    tc.assertEqual(naive_topk(students, 1, get_age),
                   topk(students, 1, get_age))

    tc.assertEqual(naive_topk(students, 3, get_age),
                   topk(students, 3, get_age))

################################################################################
# TEST HELPERS
################################################################################


def say_test(f):
    print(80 * "*" + "\n" + f.__name__)


def say_success():
    print("SUCCESS")

################################################################################
# MAIN
################################################################################


def main():
    for t in [test_key_heap_1,
              test_key_heap_2,
              test_key_heap_3,
              test_key_heap_4,
              test_key_heap_5,
              test_median_1,
              test_median_2,
              test_median_3,
              test_topk_students
              ]:
        say_test(t)
        t()
        say_success()


if __name__ == '__main__':
    main()
