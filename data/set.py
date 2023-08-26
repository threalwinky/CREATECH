from vector import genNum
setE = {
    "0":["Hãy liệt kê tất cả phần tử nguyên của tập hợp dưới đây.\n"]
}
equationD = {
    "0":["(2x - x^2)(2x^2-3x-2)=0"]
}

#Experiment
def makeEquation(layer = 0):
    if layer == 0:
        for i in range(genNum([1,5])):
            eq = makeEquation(1)
    elif layer == 1:
        for i in range(genNum([1,3])+1):
            a = [genNum([1,2]),genNum([3,12]),genNum([1,2]),genNum([3,12])]

