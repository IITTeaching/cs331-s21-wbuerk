import unittest
import sys
import math
from contextlib import contextmanager
from io import StringIO

#################################################################################
# TESTING OUTPUTS
#################################################################################


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

#################################################################################
# EXERCISE 1
#################################################################################

# implement this function

# tests passed


def is_perfect(n):
    if(n <= 0):
        return False
    else:
        sum = 0
        for i in range(1, n):
            if(n % i == 0):
                sum += i
        if (sum == n):
            return True
        else:
            return False
    return False


# (3 points)


def test1():
    tc = unittest.TestCase()
    for n in (6, 28, 496):
        tc.assertTrue(is_perfect(n), '{} should be perfect'.format(n))
    for n in (1, 2, 3, 4, 5, 10, 20):
        tc.assertFalse(is_perfect(n), '{} should not be perfect'.format(n))
    for n in range(30, 450):
        tc.assertFalse(is_perfect(n), '{} should not be perfect'.format(n))

#################################################################################
# EXERCISE 2
#################################################################################

# implement this function

# tests passed


def multiples_of_3_and_5(n):
    sum = 0
    for i in range(n):
        if (i % 3 == 0 or i % 5 == 0):
            sum += i
    return sum

# (3 points)


def test2():
    tc = unittest.TestCase()
    tc.assertEqual(multiples_of_3_and_5(10), 23)
    tc.assertEqual(multiples_of_3_and_5(500), 57918)
    tc.assertEqual(multiples_of_3_and_5(1000), 233168)

#################################################################################
# EXERCISE 3
#################################################################################

# tests passed


def integer_right_triangles(p):
    total = 0
    for a in range(1, int(p/2+1)):
        for b in range(1, a):
            c = p - a - b
            if c == (math.sqrt((a**2+b**2))):
                total += 1
    return total


def test3():
    tc = unittest.TestCase()
    tc.assertEqual(integer_right_triangles(60), 2)
    tc.assertEqual(integer_right_triangles(100), 0)
    tc.assertEqual(integer_right_triangles(180), 3)

#################################################################################
# EXERCISE 4
#################################################################################

# implement this function

# in progress

# Current Plan: Make a string with all of the "."s and then replace all the letters working out from the center


def two_d_to_string(two_d):
    final = ""
    for i in range(len(two_d)):
        for j in range(len(two_d[0])):
            final += str(two_d[i][j])
    return final


# printing generates correct patten but it is not coming out equal
def gen_pattern(chars):

    currentLine = list("")
    tempChars = list(chars)
    length = len(chars)
    width = (length*2-1)+((length-1)*2)
    center = int(width/2)
    height = length*2-1

    # create pattern as a 2d list of dots
    pattern = list()
    for i in range(height):
        pattern.append(list(""))
        for j in range(width):
            pattern[i] += "."

        pattern[i] += "\n"

    # top half of pattern
    for h in range(length):
        for i in range(length-h):
            for j in range(i+1):
                pattern[i+h][center+(2*i)] = tempChars[length-1-h]
                pattern[i+h][center-(2*i)] = tempChars[length-1-h]

    # bottom half of pattern
    for h in range(length):
        # rows
        for i in range(height, int(height/2)+h, -1):
            # from center column out in increments of two
            for j in range(i+1):

                pattern[i-1-h][center+(2*(height-i))] = tempChars[length-1-h]
                pattern[i-1-h][center-(2*(height-i))] = tempChars[length-1-h]

    final = (two_d_to_string(pattern)).rstrip()
    print(final)


def test4():
    tc = unittest.TestCase()
    with captured_output() as (out, err):
        gen_pattern('@')
        tc.assertEqual(out.getvalue().strip(), '@')
    with captured_output() as (out, err):
        gen_pattern('@%')
        tc.assertEqual(out.getvalue().strip(),
                       """
..%..
%.@.%
..%..
""".strip())
    with captured_output() as (out, err):
        gen_pattern('ABC')
        tc.assertEqual(out.getvalue().strip(),
                       """
....C....
..C.B.C..
C.B.A.B.C
..C.B.C..
....C....
""".strip())
    with captured_output() as (out, err):
        gen_pattern('#####')
        tc.assertEqual(out.getvalue().strip(),
                       """
........#........
......#.#.#......
....#.#.#.#.#....
..#.#.#.#.#.#.#..
#.#.#.#.#.#.#.#.#
..#.#.#.#.#.#.#..
....#.#.#.#.#....
......#.#.#......
........#........
""".strip())
    with captured_output() as (out, err):
        gen_pattern('abcdefghijklmnop')
        tc.assertEqual(out.getvalue().strip(),
                       """
..............................p..............................
............................p.o.p............................
..........................p.o.n.o.p..........................
........................p.o.n.m.n.o.p........................
......................p.o.n.m.l.m.n.o.p......................
....................p.o.n.m.l.k.l.m.n.o.p....................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p
..p.o.n.m.l.k.j.i.h.g.f.e.d.c.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p..
....p.o.n.m.l.k.j.i.h.g.f.e.d.c.d.e.f.g.h.i.j.k.l.m.n.o.p....
......p.o.n.m.l.k.j.i.h.g.f.e.d.e.f.g.h.i.j.k.l.m.n.o.p......
........p.o.n.m.l.k.j.i.h.g.f.e.f.g.h.i.j.k.l.m.n.o.p........
..........p.o.n.m.l.k.j.i.h.g.f.g.h.i.j.k.l.m.n.o.p..........
............p.o.n.m.l.k.j.i.h.g.h.i.j.k.l.m.n.o.p............
..............p.o.n.m.l.k.j.i.h.i.j.k.l.m.n.o.p..............
................p.o.n.m.l.k.j.i.j.k.l.m.n.o.p................
..................p.o.n.m.l.k.j.k.l.m.n.o.p..................
....................p.o.n.m.l.k.l.m.n.o.p....................
......................p.o.n.m.l.m.n.o.p......................
........................p.o.n.m.n.o.p........................
..........................p.o.n.o.p..........................
............................p.o.p............................
..............................p..............................
""".strip()
        )

#################################################################################
# RUN ALL TESTS
#################################################################################


def main():
    test1()
    test2()
    test3()
    test4()


if __name__ == '__main__':
    main()
