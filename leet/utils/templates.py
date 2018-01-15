def fail_string(res, ans, case=None):
    out = (
        '\n---TEST FAILED---\n'
        'Case:     {case}\n'
        'Result:   {res}\n'
        'Expected: {ans}\n'
        '-----------------'
        ).format(res=res, ans=ans, case=case if case else '')

    return out

def debug(what, flag):
    if flag:
        print what