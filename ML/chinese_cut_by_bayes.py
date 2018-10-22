import os
import jieba
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split

#读取数据集
data_path = input(r"请输入数据集绝对路径，如C:\Users\zzp\OneDrive\Desktop\课件\机器学习\作业\2第四五章练习题\data")
data_x = []
data_y = []
for root,dirs,files in os.walk(data_path):
    rootname = os.path.basename(root)
    for file in files:
        filepath = os.path.join(root,file)
        with open(filepath,errors="ignore") as f:
            text = f.read()
            word_cut = jieba.cut(text,cut_all=False)  #分词结果中包含标点，待处理
            word_list = list(word_cut)
            data_x.append(word_list)
        data_y.append(rootname)


#训练集、测试机划分
x_train,x_test,y_train,y_test = train_test_split(data_x,data_y,test_size=0.3)

#数据预处理
    #词频统计，放入word_dic
word_dic = {}
for text in x_train:
    for word in text:
        if word in word_dic:
            word_dic[word] += 1
        else:
            word_dic[word] = 1
    #将word_dic按照词频降序排列,去除
word_dic_tuple_list = sorted(word_dic.items(),key=lambda f:f[1],reverse=True)
word_dic_list = list(list(zip(*word_dic_tuple_list))[0])


    #构成词袋。打印出词频/词袋，手工筛选要剔除的词组，剔除前40个和4000以后的，构成词袋。后续考虑剔除停止词
# for i in range(len(word_dic)):
#     print(i," ",word_dic_list[i],"  ",word_dic[word_dic_list[i]])
word_dic_list_bag = word_dic_list[40:1000]

    #映射文本特征，构成特征矩阵
x_train_array,x_test_array = [],[]
x_train_array1,x_test_array1 = [],[]
for x in x_train:
    x_words = set(x)
    features = [1 if word in x_words else 0 for word in word_dic_list_bag]
    x_train_array.append(features)
    features = [x.count(word) for word in word_dic_list_bag]
    x_train_array1.append(features)

for x in x_test:
    x_words = set(x)
    features = [1 if word in x_words else 0 for word in word_dic_list_bag]
    x_test_array.append(features)
    features = [x.count(word) for word in word_dic_list_bag]
    x_test_array1.append(features)

#调用sklearn库的多项式贝叶斯模型进行学习并验证
mnb = MultinomialNB(fit_prior=True)
mnb.fit(x_train_array,y_train)
print("\n\n\n多项式布尔输入模型准确率：",mnb.score(x_test_array,y_test))
mnb.fit(x_train_array1,y_train)
print("\n\n\n多项式输入模型准确率：",mnb.score(x_test_array1,y_test))
bnb = BernoulliNB(fit_prior=True)
bnb.fit(x_train_array,y_train)
print("\n\n\n伯努利模型准确率：",bnb.score(x_test_array,y_test))