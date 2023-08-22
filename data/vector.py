import numpy as np
import random

def genNum(range = [-10000,10000], step = 1):
    if isinstance(step, int):
        return random.randrange(range[0],range[1],step)
    else:
        return random.randrange(int(range[0]/step),int(range[1]/step),1)*step
    
# [Vector1, Vector2], VectorAns
#LVL1
def VectorDotND(rane= [-10^4,10^4], step = 1, n = 10):
    #[Operation, Answer]
    vector = []
    for i in range(2):
        vector.append(np.ones(n))
        for j in range(n):
            vector[i][j] = genNum(rane,step)
    dotproduct = np.dot(vector[0],vector[1])
    for i in range(2):
        vector[i] = vector[i].tolist()
    return vector, dotproduct
def VectorPlusND(rane=[-100,100],step=1,n=10):
    vector = [[],[]]
    for i in range(2):
        for j in range(n):
            vector[i].append(genNum(rane,step))
    return vector, [vector[0][i]+vector[1][i] for i in range(n)]
def VectorSubtractND(rane=[-100,100],step=1,n=10):
    vector = [[],[]]
    for i in range(2):
        for j in range(n):
            vector[i].append(genNum(rane,step))
    return vector, [vector[0][i]-vector[1][i] for i in range(n)]
#LVL2
#Currently no plan