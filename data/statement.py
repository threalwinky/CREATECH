from vector import genNum

statementE = {
    "0":["Mệnh đề sau đây đúng hay sai: Nếu số a chia hết cho 3 thì a chia hết cho 6.", "Sai", "Một số chia hết cho 6 khi và chỉ khi số đó chia hết cho cả 2 và 3."],
    "1":["Cho 2 mệnh đề: \nP: “ABCD có tổng hai góc đối bằng 180°”\nQ: “ABCD là tứ giác nội tiếp.”\nPhát biểu P => Q. Mệnh đề kéo theo này đúng hay sai?", "Đúng", "P => Q: Nếu tứ giác ABCD có tổng hai góc đối bằng 180° thì ABCD là tứ giác nội tiếp."]
}
def StatementE(t=1):
    task = statementE[str(t)]
    return task