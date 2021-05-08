import urllib
import requests
from unittest import TestCase


def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii', 'replace')
    return bookascii.split()


def max_length(lst):
    max_len = 0

    for word in lst:
        length = len(word)
        if length > max_len:
            max_len = length

    return max_len


def rolling_sum(lst):

    if len(lst) < 1:
        raise ValueError

    for x in range(1, len(lst)):
        lst[x] += lst[x-1]

    return lst


def counting_sort(lst, index):
    counting_list = [0] * 257
    aux_list = [None] * len(lst)

    for word in lst:
        try:
            # byte = ord(word[index])
            byte = word[index]
        except IndexError:
            byte = -1

        counting_list[byte + 1] += 1

    counting_list = rolling_sum(counting_list)

    for x in range(len(lst)-1, -1, -1):
        word = lst[x]
        try:
            # byte = ord(word[index])
            byte = word[index]
        except IndexError:
            byte = -1

        idx = counting_list[byte+1]
        aux_list[idx-1] = word
        counting_list[byte+1] += -1

    return aux_list


def radix_sort(lst):
    max_len = max_length(lst)

    for x in range(max_len-1, -1, -1):
        lst = counting_sort(lst, x)

    return lst


def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    return radix_sort(book_to_words(book_url))


if __name__ == "__main__":

    tc = TestCase()

    lst = [b'asldjsdakflj', b'a', b'baby', b'zebra',
           b'zany', b'apple', b'apply', b'apps', b'ashed']

    radixed_list = radix_sort(lst)
    sorted_list = sorted(lst)

    tc.assertEqual(radixed_list, sorted_list)
    print("#" * 80)
    print("Test Case 1 Succesful!")
    print("#" * 80)

    tc = TestCase()

    radixed_book = radix_a_book()
    sorted_book = sorted(book_to_words())

    tc.assertEqual(radixed_book, sorted_book)
    print("#" * 80)
    print("Radixed Book Succesfully!")
    print("#" * 80)
