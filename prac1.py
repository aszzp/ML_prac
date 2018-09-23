import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder


tb_mapping = {"Yes":1,"No":0,"master":3,"bachlor":4,"phd":5,"C++":6,"Java":7}
tb_inverse = {1:"Yes",0:"No",3:"master",4:"bachlor",5:"phd",6:"C++",7:"Java"}

tb=pd.read_csv('E:\career_data1.csv',header=None)   #待进一步修正

#class_label = LabelEncoder()
for i in range(tb.columns.size):
    tb[i] =tb[i].map(tb_mapping)

x=tb[[0,1,2]]
#['985','education','skill'
#print(x)
y=tb[3]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25)

# vec = CountVectorizer()
# x_train = vec.fit_transform(x_train)
# y_train = vec.fit_transform(y_train)
# x_test = vec.transform(x_test)

mnb=MultinomialNB(fit_prior=True)
mnb.fit(x_train,y_train)
y_predict=mnb.predict(x_test)

test=[]
for i in range(x_test.iloc[:,0].size):
    test = x_test.iloc[i].map(tb_inverse)
    print(test,"\n",y_predict[i])
