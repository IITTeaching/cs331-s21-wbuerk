import random
from unittest import TestCase

################################################################################
# EXTENSIBLE HASHTABLE
################################################################################


class ExtensibleHashTable:

    def __init__(self, n_buckets=1000, fillfactor=0.5):
        self.n_buckets = n_buckets
        self.fillfactor = fillfactor
        self.buckets = [None] * n_buckets
        self.nitems = 0

    def find_bucket(self, key):
        # BEGIN_SOLUTION
        return key % self.n_buckets
        # END_SOLUTION

    def __getitem__(self,  key):
        # BEGIN_SOLUTION
        bucket = self.buckets[self.find_bucket(key)]
        if bucket:
            for el in bucket:
                if el[0] == key:
                    return el[1]
        else:
            raise KeyError
        # END_SOLUTION

    def __setitem__(self, key, value):
        # BEGIN_SOLUTION
        if self.buckets[self.find_bucket(key)]:
            bucket = self.buckets[self.find_bucket(key)]
        else:
            self.buckets[self.find_bucket(key)] = []
            bucket = self.buckets[self.find_bucket(key)]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.nitems += 1

        if self.nitems / self.n_buckets > self.fillfactor:
            self.extend()
        # END_SOLUTION

    def extend(self):
        self.n_buckets *= 2
        buckets_copy = self.buckets.copy()
        self.buckets = [None] * self.n_buckets
        self.nitems = 0

        for bucket in buckets_copy:
            if bucket:
                for item in bucket:
                    if item:
                        self[item[0]] = item[1]

    def __delitem__(self, key):
        # BEGIN SOLUTION
        bucket = self.buckets[self.find_bucket(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                del(bucket[i])
                self.nitems += -1
        # END SOLUTION

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except:
            return False

    def __len__(self):
        return self.nitems

    def __bool__(self):
        return self.__len__() != 0

    def __iter__(self):
        # BEGIN SOLUTION
        for el in self.buckets:
            if el:
                for el2 in el:
                    yield el2[0]
        # END SOLUTION

    def keys(self):
        return iter(self)

    def values(self):
        # BEGIN SOLUTION
        for key in self.keys():
            yield self[key]
        # END SOLUTION

    def items(self):
        # BEGIN SOLUTION
        for el in self.buckets:
            if el:
                for el2 in el:
                    yield el2
        # END SOLUTION

    def __str__(self):
        return '{ ' + ', '.join(str(k) + ': ' + str(v) for k, v in self.items()) + ' }'

    def __repr__(self):
        return str(self)

################################################################################
# TEST CASES
################################################################################
# points: 20


def test_insert():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100000)

    for i in range(1, 10000):
        h[i] = i
        tc.assertEqual(h[i], i)
        tc.assertEqual(len(h), i)

    random.seed(1234)
    for i in range(1000):
        k = random.randint(0, 1000000)
        h[k] = k
        tc.assertEqual(h[k], k)

    for i in range(1000):
        k = random.randint(0, 1000000)
        h[k] = "testing"
        print(k)
        print(h.buckets[h.find_bucket(k)])
        tc.assertEqual(h[k], "testing")

# points: 10


def test_getitem():
    tc = TestCase()
    h = ExtensibleHashTable()

    for i in range(0, 100):
        h[i] = i * 2

    with tc.assertRaises(KeyError):
        h[200]


# points: 10
def test_iteration():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100)
    entries = [(random.randint(0, 10000), i) for i in range(100)]
    keys = [k for k, v in entries]
    values = [v for k, v in entries]

    for k, v in entries:
        h[k] = v

    for k, v in entries:
        tc.assertEqual(h[k], v)

    tc.assertEqual(set(keys), set(h.keys()))
    tc.assertEqual(set(values), set(h.values()))
    tc.assertEqual(set(entries), set(h.items()))

# points: 20


def test_modification():
    tc = TestCase()
    h = ExtensibleHashTable()
    random.seed(1234)
    keys = [random.randint(0, 10000000) for i in range(100)]

    for i in keys:
        h[i] = 0

    for i in range(10):
        for i in keys:
            h[i] = h[i] + 1

    for k in keys:
        tc.assertEqual(h[k], 10)

# points: 20


def test_extension():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100, fillfactor=0.5)
    nitems = 10000
    for i in range(nitems):
        h[i] = i

    tc.assertEqual(len(h), nitems)
    tc.assertEqual(h.n_buckets, 25600)

    for i in range(nitems):
        tc.assertEqual(h[i], i)


# points: 20
def test_deletion():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100000)
    random.seed(1234)
    keys = [random.randint(0, 1000000) for i in range(10)]
    for k in keys:
        h[k] = 1

    for k in keys:
        del h[k]

    tc.assertEqual(len(h), 0)
    with tc.assertRaises(KeyError):
        h[keys[0]]

    with tc.assertRaises(KeyError):
        h[keys[3]]

    with tc.assertRaises(KeyError):
        h[keys[5]]

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
    for t in [test_insert,
              test_iteration,
              test_getitem,
              test_modification,
              test_deletion,
              test_extension]:
        say_test(t)
        t()
        say_success()


if __name__ == '__main__':
    main()
