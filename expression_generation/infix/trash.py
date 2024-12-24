# almost works
def add_parentheses(s: list):
    if len(s) % 2 == 0:
        raise Exception("Did you add the right number of operations for each element?", s)
    if len(s) < 5:
        return []
    if len(s) == 3 * 2 - 1:
        ret = [s.copy(), s.copy()]
        ret[0].insert(0, "(")
        ret[0].insert(4, ")")
        ret[1].insert(2, "(")
        ret[1].insert(6, ")")

        print(ret)
        return ret

    return [add_parentheses(s[:-4]), add_parentheses(s[2:])]
