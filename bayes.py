import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
#定义字符属性到数值属性的映射字典
tb_mapping = {"Yes":1,"No":0,"master":3,"bachlor":4,"phd":5,"C++":6,"Java":7}
tb_inverse = {1:"Yes",0:"No",3:"master",4:"bachlor",5:"phd",6:"C++",7:"Java"}

#读取数据集，并略去列名所在的第一行
print("请输入数据集csv文件地址，格式如e:/career_data.csv")
input_add=input()
print(input_add)
tb=pd.read_csv(input_add,skiprows=1,header=None)

#逐列对读取的表格进行属性映射，转换为贝叶斯模型可以使用的数值型。
for i in range(tb.columns.size):
    tb[i] =tb[i].map(tb_mapping)

#将前三列取出作为属性矩阵，第四列作为分类结果，并划分为训练集合验证集。
x,y = tb[[0,1,2]],tb[3]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25)

#使用贝叶斯多项式模型进行训练，并在测试集上验证
mnb=MultinomialNB(fit_prior=True)
mnb.fit(x_train,y_train)
y_predict=mnb.predict(x_test)

#输出结果
for i in range(x_test.iloc[:,0].size):
    test = x_test.iloc[i].map(tb_inverse)
    result =tb_inverse[y_predict[i]]
    print("\n\n测试数据1：\n",test,"\n","录取结果是：",result)

print("\n\n\n模型准确率：",mnb.score(x_test,y_test))