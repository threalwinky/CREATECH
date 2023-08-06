from pprint import pprint
from unidecode import unidecode
d = """1. Đồi thuộc dạng địa hình núi già hay trẻ?

Đáp án: núi già

2. What do you call a piece of cloth used as a symbol of a country oras a signal?

Đáp án: Flag

3. World Cup 2018 được tổ chức ở nước nào?

Đáp án: Nga

4. Trẻ em từ 2-6 tuổi có bao nhiêu răng sữa?

Đáp án: 20

5. Trong truyền thuyết bà Lê Chân nữ tướng tiên phong của Hai Bà Trưng xưa kia đã dùng môn thể thao nào để tuyển binh, tuyển tướng?

Đáp án: Đấu vật

6. ... Là loại than có khả năng hấp phụ mạnh, được dùng sản xuất mặt nạ phòng độc? 

Đáp án: Than hoạt tính

7. Trên la bàn, kim chỉ hướng đông hợp với kim chỉ hướng nam 1 góc bao nhiêu độ? 

Đáp án: 90 độ

8. Trong công nghệ sản xuất máy lạnh trước đây hợp chất nào của nitơ mà dạng lỏng của nó được sử dụng làm chất gây lạnh?

Đáp án: NH3

9. Điểm phân cách giữa cung lồi và cung lõm của đồ thị hàm số được gọi là....

Đáp án: Điểm uốn

10. Khí quyển là một lớp khí bao bọc xung quanh một thiên thể có khối lượng đủ lớn và nó được giữ lại bởi..... của thiên thể đó.

Đáp án: trọng lực"""
a = d.split("\n\n")
arr = {}
for i in range(0, len(a)):
    if (a[i][0] != 'Đ'):
        arr.update({a[i]: a[i+1]}) 

for i in arr:
    print("\""+i +"\""+ ":", "\""+unidecode(arr[i].split("Đáp án: ")[1]).lower()+"\",")

# print(unidecode("Chào"))