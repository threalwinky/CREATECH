from datasets import load_dataset
import random

class LeoLib:
    linear2d = load_dataset("math_dataset","algebra__linear_2d", split="test")
    def __init__(self,random_item):
        self.random_item = random_item
    def Algebra__linear_2d(random_item = random.randrange(1,10**4)):
        return [LeoLib.linear2d['question'][random_item],LeoLib.linear2d['answer'][random_item]]

#Usage
CallLib = LeoLib
# a = random.randrange(1,10**4)
# print(CallLib.Algebra__linear_2d(a))
print(CallLib.Algebra__linear_2d())