from datasets import load_dataset
import random

class LeoLib:
    linear2d = load_dataset("math_dataset","algebra__linear_2d", split="test").shuffle(seed=42)
    def __init__(self):
        pass
    def Algebra__linear_2d():
        return next(iter(LeoLib.linear2d))
    

#Usage
CallLib = LeoLib
print(CallLib.Algebra__linear_2d())