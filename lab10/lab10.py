from unittest import TestCase
import random


class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
            self.bv = 0

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right

        def rotate_left(self):
            # BEGIN SOLUTION
            n = self.right
            self.val, n.val = n.val, self.val
            self.right, n.right, self.left, n.left = n.right, n.left, n, self.left
            # END SOLUTION

        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1+AVLTree.Node.height(n.left), 1+AVLTree.Node.height(n.right))

        def update_bv(self):
            self.bv = AVLTree.Node.height(
                self.right) - AVLTree.Node.height(self.left)

    def __init__(self):
        self.size = 0
        self.root = None

    @staticmethod
    def rebalance(t):
        # BEGIN SOLUTION

        # LL
        if t.bv < -1:
            ll = t.left.left
            lr = t.left.right
            if AVLTree.Node.height(ll) > AVLTree.Node.height(lr):
                t.rotate_right()
            else:
                t.left.rotate_left()
                t.rotate_right()

        # RR
        elif t.bv > 1:
            rr = t.right.right
            rl = t.right.left
            if AVLTree.Node.height(rr) > AVLTree.Node.height(rl):
                t.rotate_left()
            else:
                t.right.rotate_right()
                t.rotate_left()

        # END SOLUTION

    def add(self, val):
        assert(val not in self)
        # BEGIN SOLUTION

        def add_rec(node):
            if val < node.val:
                if node.left:
                    add_rec(node.left)
                    node.update_bv()
                    AVLTree.rebalance(node)
                else:
                    node.left = AVLTree.Node(val)
            if val > node.val:
                if node.right:
                    add_rec(node.right)
                    node.update_bv()
                    AVLTree.rebalance(node)
                else:
                    node.right = AVLTree.Node(val)

        if self.root:
            add_rec(self.root)
        else:
            self.root = AVLTree.Node(val)
        self.size += 1

        # END SOLUTION

    def __delitem__(self, val):
        assert(val in self)
        # BEGIN SOLUTION

        def delitem_rec(node):
            if val < node.val:
                scenario = delitem_rec(node.left)
                if scenario == 1:
                    node.left = None
                node.update_bv()
                AVLTree.rebalance(node)
                return 0

            elif val > node.val:
                scenario = delitem_rec(node.right)
                if scenario == 1:
                    node.right = None
                node.update_bv()
                AVLTree.rebalance(node)
                return 0

            else:
                if not node.left and not node.right:
                    # broken
                    return 1
                elif node.left and not node.right:
                    """t = node.left
                    if not t.right:
                        node.val = t.val
                        node.left = t.left
                    else:
                        n = t
                        if not n.right.right:
                            node.val = node.left.right.val
                            node.left.right = None

                        else:
                            while n.right.right:
                                n = n.right
                                t = n.right
                            n.right = t.left
                            node.val = t.val"""

                    node.val = node.left.val
                    node.left = node.left.left
                elif node.right and not node.left:
                    """t = node.right
                    if not t.left:
                        node.val = t.val
                        node.right = t.right
                    else:
                        n = t
                        if not n.left.left:
                            node.val = node.right.left.val
                            node.right.left = None

                        else:
                            while n.left.left:
                                n = n.left
                                t = n.left
                            n.left = t.right
                            node.val = t.val"""

                    node.val = node.right.val
                    node.right = node.right.right
                else:
                    t = node.left
                    if not t.right:
                        node.val = t.val
                        node.left = t.left
                    else:
                        n = t
                        if not n.right.right:
                            node.val = node.left.right.val
                            node.left.right = node.left.right.left

                        else:
                            while n.right.right:
                                n = n.right
                                t = n.right
                            n.right = t.left
                            node.val = t.val

                if node:
                    node.update_bv()
                    AVLTree.rebalance(node)

                    return 2

        delitem_rec(self.root)
        self.size += -1
        # END SOLUTION

    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)

    def __len__(self):
        return self.size

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
        yield from iter_rec(self.root)

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n, level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(
                    val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(
                    val=n.val, width=width//2**level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)

################################################################################
# TEST CASES
################################################################################


def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))


def traverse(t, fn):
    if t:
        fn(t)
        traverse(t.left, fn)
        traverse(t.right, fn)

# LL-fix (simple) test
# 10 points


def test_ll_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 2, 1]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RR-fix (simple) test
# 10 points


def test_rr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 2, 3]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# LR-fix (simple) test
# 10 points


def test_lr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 1, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RL-fix (simple) test
# 10 points


def test_rl_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 3, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# ensure key order is maintained after insertions and removals
# 30 points


def test_key_order_after_ops():
    tc = TestCase()
    vals = list(range(0, 100000000, 333333))
    random.shuffle(vals)

    t = AVLTree()
    for x in vals:
        t.add(x)

    for _ in range(len(vals) // 3):
        to_rem = vals.pop(random.randrange(len(vals)))
        del t[to_rem]
        t.pprint()

    vals.sort()

    for i, val in enumerate(t):
        tc.assertEqual(val, vals[i])

# stress testing
# 30 points


def test_stress_testing():
    tc = TestCase()

    def check_balance(t):
        tc.assertLess(abs(height(t.left) - height(t.right)),
                      2, 'Tree is out of balance')

    t = AVLTree()
    vals = list(range(1000))
    random.shuffle(vals)
    for i in range(len(vals)):
        t.add(vals[i])
        for x in vals[:i+1]:
            tc.assertIn(x, t, 'Element added not in tree')
        traverse(t.root, check_balance)

    random.shuffle(vals)
    for i in range(len(vals)):
        del t[vals[i]]
        for x in vals[i+1:]:
            tc.assertIn(x, t, 'Incorrect element removed from tree')
        for x in vals[:i+1]:
            tc.assertNotIn(x, t, 'Element removed still in tree')
        traverse(t.root, check_balance)


################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")


def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################


def personal_tests():
    t = AVLTree()
    for x in range(20):
        t.add(x)
        t.pprint()

    random_numbers = random.sample(range(20), 20)
    for x in random_numbers:
        t.__delitem__(x)
        t.pprint()


def main():
    for t in [test_ll_fix_simple,
              test_rr_fix_simple,
              test_lr_fix_simple,
              test_rl_fix_simple,
              test_key_order_after_ops,
              test_stress_testing]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")


if __name__ == '__main__':
    main()
