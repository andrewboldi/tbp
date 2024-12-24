#!/usr/bin/python3

# Rewritten by ChatGPT
import os
import math
import tqdm
import operator
import itertools
from datetime import datetime

class PostfixEvaluator:
    def evaluate(self, expr, ops):
        tokens = expr.split()
        stack = []
        for token in tokens:
            if token in ops:
                if len(stack) < 2:
                    # Not enough operands
                    return None
                e2 = stack.pop()
                e1 = stack.pop()
                try:
                    result = ops[token](float(e1), float(e2))
                except (ZeroDivisionError, OverflowError):
                    result = math.inf
                stack.append(result)
            else:
                stack.append(token)
        if len(stack) != 1:
            # Invalid expression
            return None
        return stack[0]

class ExpressionGenerator:
    def __init__(self, nums, ops):
        self.nums = nums
        self.ops = ops

    def __generate_num_combos(self):
        return itertools.permutations(self.nums)

    def __generate_op_combos(self):
        return itertools.product(self.ops, repeat=len(self.nums) - 1)

    def __generate_expressions(self):
        for num_combo in self.__generate_num_combos():
            for op_combo in self.__generate_op_combos():
                expr = []
                expr.extend(num_combo)
                expr.extend(op_combo)
                yield ' '.join(expr)

    def generate(self):
        return self.__generate_expressions()

if __name__ == "__main__":
    start = datetime.now()
#    nums = ["8"] * 8  # You can change this to include different numbers
    nums = ["8", "8", "8", "8", "8", "8", "8", "8"]  # For different numbers
    ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv, "^": operator.pow}
    fname = f"{''.join(nums)}_{len(ops)}.txt"
    if os.path.isfile(fname):
        inp = input(f"File {fname} already exists.... replace the file? (Y/n): ")
        if inp.lower() != "y":
            exit(0)
    with open(fname, "w") as out:
        PE = PostfixEvaluator()
        EG = ExpressionGenerator(nums, list(ops.keys()))
        total_exprs = math.factorial(len(nums)) * len(ops) ** (len(nums) - 1)
        exprs_generated = 0
        for expr in tqdm.tqdm(EG.generate(), total=total_exprs):
            res = PE.evaluate(expr, ops)
            if res is not None:
                print(f"{expr} = {res}", file=out)
                exprs_generated += 1

        end = datetime.now()

        assert exprs_generated == total_exprs
        print(f"\nTotal Expressions: {exprs_generated} = {len(nums)}! * ({len(ops)} ^ {len(nums) - 1}) ✅\nTotal Time: {end-start}", file=out)

    print(f"Created file {fname} with {exprs_generated} expressions in {end-start}.")
