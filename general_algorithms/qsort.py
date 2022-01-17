import random

def choose_pivot(m, n):
    if m > n - 1:
        raise Exception('Invalid range ({} {})'.format(m, n))

    # randint return bound inclusive range [0, n]
    # while we don't mean to include n
    return random.randint(m + 1, n - 1)


# Let's do an in place sorting out of place will can reuse the in 
# place algorithm by making a copy
def qsort(array: list, m: int, n: int):
    # check terminal condition

    # what's the definitely terminal: 1
    if m > n - 1 or m < 0 or n > len(array):
        return
    elif m >= n - 1:
        print ('Debug: terminal', a[m:n])
        return


    # Choose a pivot using some scheme
    p = choose_pivot(m, n)

    print('Debug: sorting {}'.format(p), a[m:n])

    # move everything larger than pivot i-th to the right
    # everything else to the left
    #
    # [4   1   [0]   3   2]
    # [0        4]
    # [    1    4]
    # [         3    4    ]
    # [0   1   [2]   4   3]

    # [2   0   [1]   3   4]
    # [2   1   [2]   3   4]

    for i in range(m, p):
        if array[i] > array[p]:
            array[i], array[p] = array[p], array[i]

    for i in range(p+1, n):
        if array[i] < array[p]:
            array[i], array[p] = array[p], array[i]


    print('Debug: sorting {}'.format(p), a[m:n])


    # recurse left part
    qsort(array, m, p)

    # recurse right part
    qsort(array, p, n)

    # merge


if __name__ == '__main__':
    a = [2, 4, 1]

    # qsort(a, 0, len(a))

    # # assert a == [1, 2, 4]
    # print(a)
    # assert len(a) == 3
    # assert a[0] == 1
    # assert a[1] == 2
    # assert a[2] == 4

    a = [4, 1, 5, 0, 9, 6, 3, 2]
    qsort(a, 0, len(a))
    assert a == sorted(a), a
