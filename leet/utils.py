def fail_string(res, ans):
    out = (
        '\n---TEST FAILED---\n'
        'Result:   {}\n'
        'Expected: {}\n'
        '-----------------'
        ).format(res, ans)

    return out