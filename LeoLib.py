from datasets import load_dataset
import random, qrcode

class LeoLib:
    linear2d = load_dataset("math_dataset","algebra__linear_2d", split="test")
    def __init__(self,random_item,link):
        self.random_item = random_item
        self.link=link
    def Algebra__linear_2d(random_item = random.randrange(1,10**4)):
        return [
            LeoLib.linear2d['question'][random_item],
            LeoLib.linear2d['answer'][random_item]
            ]
    def MakeQR(link):
        qrimage = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2
            )
        qrimage.add_data(link)
        qrimage = qrimage.make_image(fill_color='black', back_color='white')
        return qrimage
#Usage
CallLib = LeoLib
# a = random.randrange(1,10**4)
# print(CallLib.Algebra__linear_2d(a))
print(CallLib.Algebra__linear_2d())
try:
    LeoLib.MakeQR("https://youtube.com/").show()
except:
    break