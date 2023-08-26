# from pprint import pprint
# from unidecode import unidecode
# d = """1. Đồi thuộc dạng địa hình núi già hay trẻ?

# Đáp án: núi già

# 2. What do you call a piece of cloth used as a symbol of a country oras a signal?

# Đáp án: Flag

# 3. World Cup 2018 được tổ chức ở nước nào?

# Đáp án: Nga

# 4. Trẻ em từ 2-6 tuổi có bao nhiêu răng sữa?

# Đáp án: 20

# 5. Trong truyền thuyết bà Lê Chân nữ tướng tiên phong của Hai Bà Trưng xưa kia đã dùng môn thể thao nào để tuyển binh, tuyển tướng?

# Đáp án: Đấu vật

# 6. ... Là loại than có khả năng hấp phụ mạnh, được dùng sản xuất mặt nạ phòng độc? 

# Đáp án: Than hoạt tính

# 7. Trên la bàn, kim chỉ hướng đông hợp với kim chỉ hướng nam 1 góc bao nhiêu độ? 

# Đáp án: 90 độ

# 8. Trong công nghệ sản xuất máy lạnh trước đây hợp chất nào của nitơ mà dạng lỏng của nó được sử dụng làm chất gây lạnh?

# Đáp án: NH3

# 9. Điểm phân cách giữa cung lồi và cung lõm của đồ thị hàm số được gọi là....

# Đáp án: Điểm uốn

# 10. Khí quyển là một lớp khí bao bọc xung quanh một thiên thể có khối lượng đủ lớn và nó được giữ lại bởi..... của thiên thể đó.

# Đáp án: trọng lực"""
# a = d.split("\n\n")
# arr = {}
# for i in range(0, len(a)):
#     if (a[i][0] != 'Đ'):
#         arr.update({a[i]: a[i+1]}) 

# for i in arr:
#     print("\""+i +"\""+ ":", "\""+unidecode(arr[i].split("Đáp án: ")[1]).lower()+"\",")

# # print(unidecode("Chào"))


progressionE = {
    "0":["Viết các số chẵn bắt đầu từ {}. Số cuối cùng là {}. Dãy số có bao nhiêu số?", " số"],
    "1":["Cho dãy số {s}, {s1}, {s2}, {s3}, ..., {e}. Hỏi dãy số có bao nhiêu số hạng?", " số"],
    "2":["Cho dãy số: {}, {}, {}, ... \nTìm số hạng thứ {} của dãy.", ""],
    "3":["Tính nhanh tổng sau: {} + {} + {} + ... + {}", ""],
    "4":["Tính nhanh các tổng sau: /n{} + {} + {} + ... + {} /n{} + {} + {} + ... + {} /n{} + {} + {} + ... + {}", ""],
    "5":["Cho dãy số: {}, {}, {}, ... \n{} là số hạng thứ mấy của dãy?", "thứ "]
}

import random
from vector import genNum
import math

def ProgressionE(t=random.randrange(0,5)):
    task = progressionE[str(t)]
    if t == 0:
        s, e = genNum([1,10]), genNum([12,999])
        task[0] = task[0].format(s,e)
        task[1] = str(math.floor((e-s)/2+1)) + task[1]
    elif t == 1:
        s,k,n = genNum([1,10]), genNum([1,4]),genNum([10,200])
        task[0] = task[0].format(s=s, s1 = s+k, s2 = s+2*k, s3=s+3*k, e = s+(n-1)*k)
        task[1] = str(n) + task[1]
    elif t == 2:
        s,k,n = genNum([1,10]), genNum([1,4]),genNum([10,200])
        task[0] = task[0].format(s,s+k,s+2*k,n)
        task[1] = str(s + (n-1) * k) + task[1]
    elif t == 3:
        s,k,n = genNum([1,10]), genNum([1,4]),genNum([10,200])
        task[0] = task[0].format(s,s+k,s+2*k,s+(n-1)*k)
        task[1] = str((2*s + (n-1)*k)*n/2) + task[1]
    elif t == 4:
        s,k,n = genNum([1,10]), genNum([1,4]),genNum([10,200])
        s1,k1,n1 = genNum([1,10]), genNum([1,4]),genNum([10,200])
        s2,k2,n2 = genNum([1,10]), genNum([1,4]),genNum([10,200])
        task[0] = task[0].format(s,s+k,s+2*k,s+(n-1)*k,
                                 s1,s1+k1,s1+2*k1,s1+(n1-1)*k1,
                                 s2,s2+k2,s2+2*k2,s2+(n2-1)*k2)
        task[1] = str((2*s + (n-1)*k)*n/2) +" " +str((2*s1 + (n1-1)*k1)*n1/2) + " "+str((2*s2 + (n2-1)*k2)*n2/2) + task[1]
    elif t == 5:
        s,k,n = genNum([1,10]), genNum([1,4]),genNum([10,200])
        task[0] = task[0].format(s,s+k, s+2*k, s+(n-1)*k)
        task[1] += str(n)
    return task

progressionM = {
    "0":[["Người ta viết {w} thành một dãy, mỗi chữ cái được viết bằng 1 màu theo thứ tự {c1}, {c2}, {c3}. Hỏi chữ thứ {n} là chữ gì, màu gì?", "Chữ {c}, Màu {m}"]
    , ["Một người viết liên tiếp nhóm chữ {w} thành dãy {w} {w}... \n Chữ cái thứ 1000 trong dãy là chữ gì?", "Chữ {c}"]]
}
Mdata = {
    "0":[["TOÁN LỚP 10","TOÁN HỌC","Pythagoras","KHOA HỌC",
    "HỌC ĐỂ CỐNG HIẾN", "TỔ QUỐC VIỆT NAM"],
    ["đỏ", "tím", "vàng", "hồng", "xanh lam", "xanh trời",
     "xanh lá", "xanh biển", "trắng", "cam", "kim"]]
}

def ProgressionM(t=0):
    task = random.choice(progressionM[str(t)])
    if t == 0:
        word, color = random.choice(Mdata["0"][0]), random.choices(Mdata["0"][1], k=3)
        n = genNum([10,22000])
        task[0].format(w=word, c1=color[0],c2=color[1],c3=color[2], n = n)
        task[1].format(c=word[n%len(word)-1],m=color[n%3-1])
    return task
