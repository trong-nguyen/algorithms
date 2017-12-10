def bisect(array, v, default):
    if array[-1] <= v:
        return default

    if array[0] > v:
        return array[0]

    if len(array) < 3:
        for a in array:
            if a > v:
                return a


    midx = len(array)/2
    mid = array[midx]
    if v >= mid:
        return bisect(array[midx+1:], v, default)
    else:
        return bisect(array[:midx+1], v, default)

def test():
    for (letters, target), ans in [
        ((["c", "f", "j"], "a"), "c"),
        ((["c", "f", "j"], "c"), "f"),
        ((["e","e","e","e","e","e","n","n","n","n"], "n"), "e"),
        ((["e","e","e","k","q","q","q","v","v","y"], "q"), "v"),
    ]:
        # res = bisect([letters[-1]] + letters + [letters[0]], target)
        res = bisect(letters, target, letters[0])
        assert res == ans, 'expected {}'.format(ans)

if __name__ == '__main__':
    test()