from unittest import TestCase


################################################################################
# STACK IMPLEMENTATION (DO NOT MODIFY THIS CODE)
################################################################################
class Stack:
    class Node:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next

    def __init__(self):
        self.top = None

    def push(self, val):
        self.top = Stack.Node(val, self.top)

    def pop(self):
        assert self.top, 'Stack is empty'
        val = self.top.val
        self.top = self.top.next
        return val

    def peek(self):
        return self.top.val if self.top else None

    def empty(self):
        return self.top == None

    def __bool__(self):
        return not self.empty()

    def __repr__(self):
        if not self.top:
            return ''
        return '--> ' + ', '.join(str(x) for x in self)

    def __iter__(self):
        n = self.top
        while n:
            yield n.val
            n = n.next

################################################################################
# CHECK DELIMITERS
################################################################################


def check_delimiters(expr):
    """Returns True if and only if `expr` contains only correctly matched delimiters, else returns False."""
    delim_openers = '{([<'
    delim_closers = '})]>'

    # BEGIN SOLUTION
    s = Stack()
    for c in expr:
        if c == '(' or c == '{' or c == '[' or c == '<':
            s.push(c)
        if (c in delim_closers) and s.empty():
            return False
        if (c == ')' and s.peek() == '(') or (c == '}' and s.peek() == '{') or (c == ']' and s.peek() == '[') or (c == '>' and s.peek() == '<'):
            if s.empty():
                return False
            s.pop()

    return s.empty()
    # END SOLUTION

################################################################################
# CHECK DELIMITERS - TEST CASES
################################################################################
# points: 5


def test_check_delimiters_1():
    tc = TestCase()
    tc.assertTrue(check_delimiters('()'))
    tc.assertTrue(check_delimiters('[]'))
    tc.assertTrue(check_delimiters('{}'))
    tc.assertTrue(check_delimiters('<>'))

# points:5


def test_check_delimiters_2():
    tc = TestCase()
    tc.assertTrue(check_delimiters('([])'))
    tc.assertTrue(check_delimiters('[{}]'))
    tc.assertTrue(check_delimiters('{<()>}'))
    tc.assertTrue(check_delimiters('<({[]})>'))

# points: 5


def test_check_delimiters_3():
    tc = TestCase()
    tc.assertTrue(check_delimiters('([] () <> [])'))
    tc.assertTrue(check_delimiters('[{()} [] (<> <>) {}]'))
    tc.assertTrue(check_delimiters('{} <> () []'))
    tc.assertTrue(check_delimiters('<> ([] <()>) <[] [] <> <>>'))

# points: 5


def test_check_delimiters_4():
    tc = TestCase()
    tc.assertFalse(check_delimiters('('))
    tc.assertFalse(check_delimiters('['))
    tc.assertFalse(check_delimiters('{'))
    tc.assertFalse(check_delimiters('<'))
    tc.assertFalse(check_delimiters(')'))
    tc.assertFalse(check_delimiters(']'))
    tc.assertFalse(check_delimiters('}'))
    tc.assertFalse(check_delimiters('>'))

# points: 5


def test_check_delimiters_5():
    tc = TestCase()
    tc.assertFalse(check_delimiters('( ]'))
    tc.assertFalse(check_delimiters('[ )'))
    tc.assertFalse(check_delimiters('{ >'))
    tc.assertFalse(check_delimiters('< )'))

# points: 5


def test_check_delimiters_6():
    tc = TestCase()
    tc.assertFalse(check_delimiters('[ ( ] )'))
    tc.assertFalse(check_delimiters('((((((( ))))))'))
    tc.assertFalse(check_delimiters('< < > > >'))
    tc.assertFalse(check_delimiters('( [] < {} )'))

################################################################################
# INFIX -> POSTFIX CONVERSION
################################################################################


def infix_to_postfix(expr):
    """Returns the postfix form of the infix expression found in `expr`"""
    # you may find the following precedence dictionary useful
    prec = {'*': 2, '/': 2,
            '+': 1, '-': 1}
    ops = Stack()
    postfix = []
    toks = expr.split()

    def postfix_test(tok):
        if tok.isdigit():
            postfix.append(tok)
        elif ops.empty() or ops.peek() == "(":
            ops.push(tok)
        elif tok == "(":
            ops.push(tok)
        elif tok == ")":
            while ops.peek() != "(":
                postfix.append(ops.pop())
            ops.pop()
        elif prec[tok] > prec[ops.peek()]:
            ops.push(tok)
        elif prec[tok] == prec[ops.peek()]:
            postfix.append(ops.pop())
            ops.push(tok)
        elif prec[tok] < prec[ops.peek()]:
            postfix.append(ops.pop())
            postfix_test(tok)
    # BEGIN SOLUTION
    for tok in toks:
        postfix_test(tok)
    while not ops.empty():
        if ops.peek() in "()":
            ops.pop()
        else:
            postfix.append(ops.pop())
    # END SOLUTION
    return ' '.join(postfix)

################################################################################
# INFIX -> POSTFIX CONVERSION - TEST CASES
################################################################################

# points: 10


def test_infix_to_postfix_1():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix('1'), '1')
    tc.assertEqual(infix_to_postfix('1 + 2'), '1 2 +')
    tc.assertEqual(infix_to_postfix('( 1 + 2 )'), '1 2 +')
    tc.assertEqual(infix_to_postfix('1 + 2 - 3'), '1 2 + 3 -')
    tc.assertEqual(infix_to_postfix('1 + ( 2 - 3 )'), '1 2 3 - +')

# points: 10


def test_infix_to_postfix_2():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix('1 + 2 * 3'), '1 2 3 * +')
    tc.assertEqual(infix_to_postfix('1 / 2 + 3 * 4'), '1 2 / 3 4 * +')
    tc.assertEqual(infix_to_postfix('1 * 2 * 3 + 4'), '1 2 * 3 * 4 +')
    tc.assertEqual(infix_to_postfix('1 + 2 * 3 * 4'), '1 2 3 * 4 * +')

    # points: 10


def test_infix_to_postfix_3():
    tc = TestCase()
    tc.assertEqual(infix_to_postfix('1 * ( 2 + 3 ) * 4'), '1 2 3 + * 4 *')
    tc.assertEqual(infix_to_postfix(
        '1 * ( 2 + 3 * 4 ) + 5'), '1 2 3 4 * + * 5 +')
    tc.assertEqual(infix_to_postfix(
        '1 * ( ( 2 + 3 ) * 4 ) * ( 5 - 6 )'), '1 2 3 + 4 * * 5 6 - *')

################################################################################
# QUEUE IMPLEMENTATION
################################################################################


class Queue:
    def __init__(self, limit=10):
        self.data = [None] * limit
        self.head = -1
        self.tail = -1

    # BEGIN SOLUTION
    # END SOLUTION

    def enqueue(self, val):
        # BEGIN SOLUTION
        """if self.tail - self.head == len(self.data) - 1:
            raise RuntimeError"""
        if (self.tail + 1 == self.head) or (self.tail == len(self.data)-1 and self.head == 0):
            raise RuntimeError
        if self.head == -1 and self.tail == -1:
            self.tail = 0
            self.head = 0
            self.data[0] = val
        else:
            if self.tail != len(self.data)-1:
                self.data[self.tail + 1] = val
                self.tail += 1
            else:
                self.data[0] = val
                self.tail = 0
        # END SOLUTION

    def dequeue(self):
        # BEGIN SOLUTION
        if self.empty():
            raise RuntimeError

        val = self.data[self.head]
        self.data[self.head] = None

        if self.head != len(self.data)-1:
            self.head += 1
        else:
            self.head = 0

        if self.empty():
            self.head = -1
            self.tail = -1

        return val
        # END SOLUTION

    def resize(self, newsize):
        assert(len(self.data) < newsize)
        # BEGIN SOLUTION
        newlist = [None] * newsize
        i = 0
        for x in iter(self):
            newlist[i] = x
            i += 1
        newlist[i] = self.data[self.tail]
        self.head = 0
        self.tail = i
        self.data = newlist
        # END SOLUTION

    def empty(self):
        # BEGIN SOLUTION
        for x in self.data:
            if x != None:
                return False
        return True
        # END SOLUTION

    def __bool__(self):
        return not self.empty()

    def __str__(self):
        if not(self):
            return ''
        return ', '.join(str(x) for x in self)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        # BEGIN SOLUTION
        if self.head <= self.tail:
            for i in range(self.head, self.tail):
                yield self.data[i]
        else:
            for i in range(self.head, len(self.data)):
                yield self.data[i]
            for i in range(self.tail):
                yield self.data[i]

        # END SOLUTION

        ################################################################################
        # QUEUE IMPLEMENTATION - TEST CASES
        ################################################################################

        # points: 13


def test_queue_implementation_1():
    tc = TestCase()

    q = Queue(5)
    tc.assertEqual(q.data, [None] * 5)

    for i in range(5):
        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(5)

    for i in range(5):
        tc.assertEqual(q.dequeue(), i)

    tc.assertTrue(q.empty())

# points: 13


def test_queue_implementation_2():
    tc = TestCase()

    q = Queue(10)

    for i in range(6):
        q.enqueue(i)

    tc.assertEqual(q.data.count(None), 4)

    for i in range(5):
        q.dequeue()

    tc.assertFalse(q.empty())
    tc.assertEqual(q.data.count(None), 9)
    tc.assertEqual(q.head, q.tail)
    tc.assertEqual(q.head, 5)

    for i in range(9):
        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(10)

    for x, y in zip(q, [5] + list(range(9))):
        tc.assertEqual(x, y)

    tc.assertEqual(q.dequeue(), 5)
    for i in range(9):
        tc.assertEqual(q.dequeue(), i)

    tc.assertTrue(q.empty())

# points: 14


def test_queue_implementation_3():
    tc = TestCase()

    q = Queue(5)
    for i in range(5):
        q.enqueue(i)
    for i in range(4):
        q.dequeue()
    for i in range(5, 9):
        q.enqueue(i)

    with tc.assertRaises(RuntimeError):
        q.enqueue(10)

    q.resize(10)

    for x, y in zip(q, range(4, 9)):
        tc.assertEqual(x, y)

    for i in range(9, 14):
        q.enqueue(i)

    for i in range(4, 14):
        tc.assertEqual(q.dequeue(), i)

    tc.assertTrue(q.empty())
    tc.assertEqual(q.head, -1)

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
    for t in [test_check_delimiters_1,
              test_check_delimiters_2,
              test_check_delimiters_3,
              test_check_delimiters_4,
              test_check_delimiters_5,
              test_check_delimiters_6,
              test_infix_to_postfix_1,
              test_infix_to_postfix_2,
              test_infix_to_postfix_3,
              test_queue_implementation_1,
              test_queue_implementation_2,
              test_queue_implementation_3]:
        say_test(t)
        t()
        say_success()


if __name__ == '__main__':
    main()
