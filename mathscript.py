from datasets import load_dataset
import random

class MathScriptCreaTeen:
    dataset = load_dataset('math_dataset', 'algebra__linear_1d', split='test')
    def __init__(self):
        pass
    def generate_problem():
        return MathScriptCreaTeen.dataset[random.randint()]