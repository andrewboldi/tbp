#!/usr/bin/python3
import re
import itertools
import sys
import math
import tqdm
from functools import lru_cache

sys.set_int_max_str_digits(100000000)

ops = ["+", "-", "*", "/"]
elements = ["8"] * 4

def create_operation_permutations():
    exprs = []
    for op_combo in itertools.product(ops, repeat=len(elements) - 1):
        e = elements.copy()

        for i, op in enumerate(op_combo):
            e.insert(2*i + 1, op)

        exprs.append(e)

    return exprs

@lru_cache(maxsize=5)
def create_parenthesis_permutations(expr: str) -> list[list[str]]:
    expr = list(expr)
    # need to only group 2...n-1 elements.
    # e.g. 8 - 8 / 8 is only grouped as (8 - 8) / 8
    # or 8 - (8 / 8) since (8 - 8 / 8) and (8) - (8) / (8)
    # are trivial.
    # Can be further reduced since order doesn't matter for all same ops.

    # TODO: function only generates one set of parantheses. we need to nest

    tmp = "".join(expr)
    for op in ops:
        tmp = tmp.replace(f"{op}", "")
    tmp = tmp.replace(")", "").replace("(", "")
    n = len(tmp)

    if len(expr) == 0:
        return []
    if len(expr) % 2 == 0:
        raise Exception("Did you add the right number of operations for each element?", expr)
    if n == 1 or n == 2:
        return [expr]
    if n >= 3:
        ret = []
#        ret.append(expr)
        
        for j in range(n - 2): # 0
            for i in range(n - j - 1): # (0, 1)
                e = expr.copy()
                e.insert(2 * i, "(")
                e.insert(2 * i + 4 + 2 * j, ")")

                # do replacement now
                spliced_string = ''.join(e[2*i + 1 : 2 * i + 4 + 2 * j])
                for reply in create_parenthesis_permutations(spliced_string):
                    s = e.copy()
                    s[2 * i + 1 : 2 * i + 4 + 2 * j] = reply[:]
#                    ret.append(s)

                    if i != 0:
                        lli = 0
                        lri = 2 * (i - 1) + 1

                        for left_of_reply in create_parenthesis_permutations(''.join(e[lli:lri])):
                            l = s.copy()
                            l[0:2*(i-1) + 1] = left_of_reply[:]
                            print(l)
                            ret.append(l)

                    """
                    if s[-1] != ")":
                        lli = 0
                        lri = 2 * (i - 1)

                        for left_of_reply in create_parenthesis_permutations(''.join(e[lli:lri])):
                            l = s.copy()
                            l[0:2*(i-1)] = left_of_reply[:]
                            print(l)
                            ret.append(l)
                            """


                    """
                    left_spliced_string_setup = ''.join(e[ : 2 * i])
                    match = re.search(r'\b\d+(?!.*\d)', left_spliced_string_setup)
                    if match:
                        end_pos = match.end()
                        left_spliced_string = left_spliced_string_setup[:end_pos]
                        left_spliced_right = left_spliced_string_setup[end_pos+1:]
                    else:
                        left_spliced_string = left_spliced_string_setup
                        left_spliced_right = ""

                    right_spliced_string = ''.join(e[2*i + 6 + 2 * j : ])

                    print(expr)
                    print(s)
                    print(left_spliced_string)
                    print(right_spliced_string)

                    for left_of_reply in create_parenthesis_permutations(left_spliced_string):
                        l = s.copy()
                        l[:2*i] = left_of_reply[:] + list(left_spliced_right)
                        print(l)
                        ret.append(l)

                    for right_of_reply in create_parenthesis_permutations(right_spliced_string):
                        r = s.copy()
                        r[2*i+6+2*j:] = right_of_reply[:]
                        print(r)
                        ret.append(r)

                    print("\n ===== \n")
                    """


        return ret

def main():
    # list of list of each expression.
    # i.e. [['8', '+', '8'], ['8', '-', '8'], ...]
    op_perms = create_operation_permutations()

    exprs = []
    ans = []
    out = open(f"{''.join(elements)}.txt", "a")
    target = 1000
    targeted_out = open(f"{target}--{''.join(elements)}.txt", "a")
    for expr in tqdm.tqdm(op_perms):
        for paren_expr in create_parenthesis_permutations(''.join(expr)):
            e = ' '.join(paren_expr).replace("( ", "(").replace(" )", ")")
            exprs.append(e)

            try:
                a = eval(e)
            except ZeroDivisionError:
                a = math.inf

            ans.append(a)
            out.write(f"{e} = {a}\n")
            if a == target:
                targeted_out.write(f"{e} = {a}\n")

    print(f"\nTotal expressions: {len(exprs)}")
    print(f"Unique results: {len(list(set(ans)))}")

if __name__ == "__main__":
    main()
