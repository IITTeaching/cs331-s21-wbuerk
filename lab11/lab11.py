from unittest import TestCase
import random


def quicksort(lst, pivot_fn):
    qsort(lst, 0, len(lst) - 1, pivot_fn)


def qsort(lst, low, high, pivot_fn):
    # BEGIN SOLUTION
    if low < high:
        print("start pivot")
        print(f"low: {low}")
        print(f"high: {high}")
        p = pivot_fn(lst, low, high)
        qsort(lst, low, p-1, pivot_fn)
        qsort(lst, p+1, high, pivot_fn)

    # END SOLUTION


def pivot_first(lst, low, high):
    # BEGIN SOLUTION

    lst[low], lst[high] = lst[high], lst[low]

    pivot = lst[high]
    i = low
    for j in range(low, high):
        if lst[j] < pivot:
            lst[i], lst[j] = lst[j], lst[i]
            i = i + 1
    lst[i], lst[high] = lst[high], lst[i]
    return i

    # END SOLUTION


def pivot_random(lst, low, high):
    # BEGIN SOLUTION
    rand = random.randint(low, high)
    lst[rand], lst[high] = lst[high], lst[rand]

    pivot = lst[high]
    i = low
    for j in range(low, high):
        if lst[j] < pivot:
            lst[i], lst[j] = lst[j], lst[i]
            i = i + 1
    lst[i], lst[high] = lst[high], lst[i]
    return i
    # END SOLUTION


def pivot_median_of_three(lst, low, high):
    # BEGIN SOLUTION
    med_lst = sorted([lst[low], lst[(low + high) // 2], lst[high]])
    med = med_lst[1]
    med_idx = lst.index(med, low, high+1)
    lst[med_idx], lst[high] = lst[high], lst[med_idx]

    pivot = lst[high]
    i = low
    for j in range(low, high):
        if lst[j] < pivot:
            lst[i], lst[j] = lst[j], lst[i]
            i = i + 1
    lst[i], lst[high] = lst[high], lst[i]
    return i
    # END SOLUTION

    ################################################################################
    # TEST CASES
    ################################################################################


def randomize_list(size):
    lst = list(range(0, size))
    for i in range(0, size):
        l = random.randrange(0, size)
        r = random.randrange(0, size)
        lst[l], lst[r] = lst[r], lst[l]
    return lst


def test_lists_with_pfn(pfn):
    lstsize = 20
    tc = TestCase()
    exp = list(range(0, lstsize))

    lst = list(range(0, lstsize))
    quicksort(lst, pfn)
    tc.assertEqual(lst, exp)

    print("test 1 passed")

    lst = list(reversed(range(0, lstsize)))
    print(lst)
    quicksort(lst, pfn)
    tc.assertEqual(lst, exp)

    print("test 2 passed")

    for i in range(0, 1):
        lst = randomize_list(lstsize)
        quicksort(lst, pfn)
        tc.assertEqual(lst, exp)

# 30 points


def test_first():
    test_lists_with_pfn(pivot_first)

# 30 points


def test_random():
    test_lists_with_pfn(pivot_random)

# 40 points


def test_median():
    test_lists_with_pfn(pivot_median_of_three)

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


def main():

    for t in [test_first,
              test_random,
              test_median]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")


if __name__ == '__main__':
    main()
