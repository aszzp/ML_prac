#冒泡排序

#输入检测函数
def getinput(a):
    while True:
        b = input(a)
        if b.isdigit():
            b = int(b)
            break
        else:
            print("输入格式有误，请重新输入")
    return b
array=[]
array_num = getinput("请输入元素数量:  ")
for i in range(array_num):
    array.append(getinput("请输入第%d个元素:  "%(i+1)))
#排序主体
for i in range(array_num-1):
    for t in range(array_num-1-i):
            if array[t+1] < array[t] :
                a = array[t]
                array[t] = array[t+1]
                array[t+1] = a
