#!/usr/bin/python3
import tqdm
import math
import os.path
import cProfile
import operator
import itertools
from datetime import datetime

class Stack:
    def __init__(self, writable=True, init=""):
        self.writable = writable
        self.__stack = [] + init.split()

    def __str__(self):
        return str(self.__stack)
    
    def push(self, ele):
        if not self.writable: raise ValueError("Unable to push to non-pushable stack. Try setting writable=True in your stack defintion :)")
        self.__stack.insert(0, ele)

    def pop(self):
        return self.__stack.pop(0) 

    def peek(self):
        return self.__stack[0]

    def size(self):
        return len(self.__stack)

class PostfixEvaluator:
    def evaluate(self, expr, ops):
        expr_stack = Stack(writable=True, init=expr)
        
        eval_stack = Stack()
        while expr_stack.size() > 0:
            if (op := expr_stack.peek()) in list(ops.keys()):
                if eval_stack.size() >= 2:
                    op = expr_stack.pop()
                    e2 = eval_stack.pop()
                    e1 = eval_stack.pop()

                    try:
                        expr_stack.push(ops[op](float(e1), float(e2)))
                    except (ZeroDivisionError, OverflowError):
                        expr_stack.push(math.inf)
                else:
                    raise ValueError("uh")
            else:
                eval_stack.push(expr_stack.pop())

        return eval_stack.pop()

class ExpressionGenerator:
    def __init__(self, nums, ops):
        self.nums = nums
        self.ops = ops

    def __generate_num_combos(self):
        return [x for x in itertools.permutations(self.nums)]

    def __generate_op_combos(self):
        return [x for x in itertools.product(self.ops, repeat=len(self.nums) - 1)]

    def __generate_expressions(self):
        return [x + y for x, y in itertools.product(self.__generate_num_combos(), self.__generate_op_combos())]

    def generate(self):
        return [' '.join(x) for x in self.__generate_expressions()]

if __name__ == "__main__":
    start = datetime.now()
    nums = ["8"] * 7
    #ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv, "^": operator.pow}
    ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
    fname = f"{''.join(nums)}_{len(ops)}.txt"
    if os.path.isfile(fname):
        inp = input(f"File {fname} already exists.... replace the file? (Y/n): ")
        if inp.lower() == "y":
            out = open(fname, "w")
            out.write("")
        else:
            exit(0)
    out = open(fname, "a")
    PE = PostfixEvaluator()
    EG = ExpressionGenerator(''.join(nums), ''.join(list(ops.keys())))
    cProfile.run("exprs = EG.generate()")
    for expr in exprs:
        res = PE.evaluate(expr, ops)
        print(f"{expr} = {res}", file=out)
    
    end = datetime.now()

    assert len(exprs) == math.factorial(len(nums)) * len(ops) ** (len(nums) - 1)
    print(f"\nTotal Expressions: {len(exprs)} = {len(nums)}! * ({len(ops)} ^ {len(nums) - 1}) ✅\nTotal Time: {end-start}", file=out)

    print(f"Created file {fname} with {len(exprs)} expressions in {end-start}.")
