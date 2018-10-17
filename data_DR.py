import struct
import numpy as np


def Get_Data_CLass1():
    f = open(r'C:\Users\zzp\OneDrive\Desktop\课件\机器学习\作业\3第六章练习题\data_class1.txt', 'rb')
    f.seek(0, 0)
    res = np.zeros([1024, 8])
    for i in range(0, 1024):
        for j in range(0, 8):
            byte = f.read(4)
            fvalue, = struct.unpack("f", byte)
            res[i][j] = fvalue
    return res, res.shape[1]


def Get_Data_CLass2():
    f = open(r'C:\Users\zzp\OneDrive\Desktop\课件\机器学习\作业\3第六章练习题\data_class2.txt', 'rb')
    f.seek(0, 0)
    res=np.zeros([1024, 8])
    for i in range(0, 1024):
        for j in range(0, 8):
            byte = f.read(4)
            fvalue, = struct.unpack("f", byte)
            res[i][j] = fvalue
    return res, res.shape[1]


def data_sta(x):
    # 将输入矩阵标准化
    m_array = x.mean(axis=0)      # 生成均值行向量
    std_x = x.std(axis=0)       # 生成标准差行向量
    for i in range(np.shape(x)[1]):
        if std_x[i]:        # 防止出现分母为0的情况
            x[:, i] = (x[:, i]-m_array[i]) / std_x[0]
    return x


def pca(res, k):
    # PCA算法主体
    x = res
    # 将输入矩阵标准化,存为1024*8的矩阵x
    x = data_sta(x)
    # 计算协方差矩阵cigema，尺寸为8*8
    cigema = x.T.dot(x)

    # 计算特征值及特征向量，提取前k维生成投影矩阵W，尺寸为8*k
    w = np.zeros([8, k])
    values, vectors = np.linalg.eig(cigema)      # 计算出特征值列表values和尺寸8*8的特征向量矩阵
    sort_index = values.argsort()[::-1]
    for i in range(k):
        w[:, i] = vectors[:, sort_index[i]]       # 8*k，按列存储了前K个最大特征值对应的特征向量

    # 计算降维后的新输出矩阵y，尺寸为1024*K
    D = x.dot(w)
    return w, D


def lad(res1, res2, d):
    # LAD算法主体
    x1 = res1
    x2 = res2
    # 生成类内均值行向量，尺寸为1*8
    m1 = res1.mean(axis=0)
    m2 = res2.mean(axis=0)
    for i in range(x1.shape[1]):
        x1[:, i] -= m1[i]
    for i in range(x2.shape[1]):
        x2[:, i] -= m2[i]
    # 生成类内散布矩阵，尺寸为8*8
    Sw = x1.T.dot(x1) + x2.T.dot(x2)
    Sb = (m1-m2).T.dot(m1-m2)
    # 计算Sw的逆与Sb矩阵积的特征值和特征向量，并取前d个最大特征值对应的特征向量生成投影矩阵w，尺寸为8*k
    values, vectors = np.linalg.eig(np.linalg.inv(Sw).dot(Sb))
    sort_index = values.argsort()[::-1]
    w = np.zeros([8, d])
    for i in range(d):
        w[:, i] = vectors[:, sort_index[i]]
    # 生成新的样本集D1，D2，尺寸为1024*d
    D1 = res1.dot(w)
    D2 = res2.dot(w)
    return w, D1, D2


def cca(res1, res2):
    # CCA算法主体
    x = res1
    y = res2
    # 将数据标准化,尺寸都是1024*8
    x = data_sta(x)
    y = data_sta(y)
    # 生成一对方差矩阵，尺寸都是8*8
    Sxx = x.T.dot(x)
    Syy = y.T.dot(y)
    Sxy = x.T.dot(y)
    Syx = y.T.dot(x)
    Sxx_inv = np.linalg.inv(Sxx)
    Syy_inv = np.linalg.inv(Syy)
    # 分别计算矩阵乘积并进行特征值分解
    x_values, x_vectors = np.linalg.eig(Sxx_inv@ Sxy@ Syy_inv@ Syx)
    y_values, y_vectors = np.linalg.eig(Syy_inv@ Syx@ Sxx_inv@ Sxy)
    x_values_index = np.argsort(x_values)[::-1]
    y_values_index = np.argsort(y_values)[::-1]
    # 生成系数列向量w，v，尺寸为8*1
    w = x_vectors[:, x_values_index[0]]
    v = y_vectors[:, y_values_index[0]]
    return w, v


def main():
    # 程序入口
    # 获取数据
    res1, shape1 = Get_Data_CLass1()
    res2, shape2 = Get_Data_CLass2()
    # 获取程序执行参数，选择哪个算法，降维维数等
    choosen = int(input("请键入序号选择算法:1.PCA 2.LAD 3.CCA"))
    # 执行PAC算法
    if choosen == 1:
        while 1:
            k = int(input("请输入降维后的维度数K"))
            if k > shape1 or k > shape2:
                print("维度数输入有误")
            else:
                break
        print("计算中：")
        w1, D1 = pca(res1, k)
        w2, D2 = pca(res2, k)
        print("结果已储存在局部变量w1,D1,w2,D2中。其中w为投影矩阵，D为降维后的样本集")
        return w1, D1, w2, D2
    # 执行LDA算法
    elif choosen == 2:
        while 1:
            d = int(input("请输入降维后的维度数d"))
            if d > shape1 or d > shape2:
                print("维度数输入有误")
            else:
                break
        print("计算中：")
        w, D1, D2 = lad(res1, res2, d)
        print("结果已储存在局部变量w,D中。其中w为投影矩阵，D为降维后的样本集")
        return w, D1, D2
    # 执行CCA算法
    elif choosen == 3:
        print("计算中")
        w, v = cca(res1, res2)
        print("结果已储存在局部变量w,v中，其中w为x的系数向量，v为y的系数向量")
        print(w, v)
        return w, v


main()
