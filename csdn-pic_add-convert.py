# -*- coding=utf-8
import re
import os
import urllib
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

# 将含有特殊符号的字符串转换成合法的正则表达式
def str_to_compile(str):
    cp = str.replace('\\', '\\\\')
    cp = cp.replace('?', '\?')
    cp = cp.replace('.', '\.')
    cp = cp.replace('*', '\*')
    cp = cp.replace('[', '\[')
    cp = cp.replace(']', '\]')
    cp = cp.replace('(', '\(')
    cp = cp.replace(')', '\)')
    cp = cp.replace('+', '\+')
    cp = cp.replace('^', '\^')
    cp = cp.replace('&', '\&')

    return cp

def blog_process(file):
    # 将本地md中的图片链接提取出并储存于urllist中，先匹配CSDN链接，在匹配本地链接
    blog_url = file
    blog_name = re.match(u'(.*)\.md$',os.path.basename(blog_url)).group(1)
    try:
        f = open(blog_url, encoding='utf-8')
        lines = f.readlines()
    except FileNotFoundError as e:
        print("夭寿啦，文件没找到！")
    f.close()



    # 更换博客图片链接


    # 利用腾讯提供的cos存储官网sdk进行批量上传
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # 设置用户属性, 包括secret_id, secret_key, region
    # appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
    secret_id = 'AKIDnQ2Yu8V5xkNrERbubJxcHqMlDlBzlCd3'     # 替换为用户的secret_id
    secret_key = 'TmxxHSfaBex780hIhmlfR3azmPvHbmQw'     # 替换为用户的secret_key
    region = 'ap-chengdu'    # 替换为用户的region/服务器地域编号
    token = None               # 使用临时秘钥需要传入Token，默认为空,可不填
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
    client = CosS3Client(config)


############删除云端图床和D盘临时文件夹
    i = 0
    compile_1 = re.compile('\[!\[.*?\]\(.*?\)\]\((.*?)\)')  # CSDN图片正则
    compile_2 = re.compile('[^\[]?!\[.*?\]\(([c-zC-Z]\:.*)\)')  # 本地图片正则
    compile_3 = re.compile('[^\[]?!\[.*?\]\((http[s]?:)([/]{1,4})(.*?)\)')  # 普通网络图片正则
    for x in range(len(lines)):
        fil1 = re.finditer(compile_1, lines[x])
        fil2 = re.finditer(compile_2, lines[x])
        fil3 = re.finditer(compile_3, lines[x])
        for l in fil1:
            lines[x] = re.sub(str_to_compile(l.group()), '![](https://pic-bucket-1257994648.cos.ap-chengdu.myqcloud.com/' + blog_name + '/' + blog_name + '_' + str(
                    i) + '.' + "png" + ')', lines[x], count=1)
            try:
                urllib.request.urlretrieve(l.group(1), "D:/临时/"+ blog_name + '/'+blog_name+'_'+str(i) + '.'+'png')
            except urllib.error.URLError as e :
                print('夭寿啦，下载失败啦！')
            # 读取图片字节流
            fp = open("D:/临时/"+blog_name+'_'+str(i) + '.'+'png', 'rb')
            client.put_object(
                Bucket='pic-bucket-1257994648',  # Bucket由bucketname-appid组成
                Body=fp,
                Key=blog_name + '/' + blog_name + '_' + str(i) + '.' + "png",
                StorageClass='STANDARD',
                ContentType='text/html; charset=utf-8'
            )
            i = i+1

        for l in fil2:
            lines[x] = re.sub(str_to_compile(l.group()),
                   '![](https://pic-bucket-1257994648.cos.ap-chengdu.myqcloud.com/' + blog_name + '/' + blog_name + '_' + str(
                       i) + '.' + "png" + ')', lines[x], count=1)
            fp = open(l.group(1), 'rb')
            client.put_object(
                Bucket='pic-bucket-1257994648',  # Bucket由bucketname-appid组成
                Body=fp,
                Key=blog_name + '/' + blog_name + '_' + str(i) + '.' + "png",
                StorageClass='STANDARD',
                ContentType='text/html; charset=utf-8'
            )
            i = i + 1

        for l in fil3:
            lines[x] = re.sub(str_to_compile(l.group()), '![](https://pic-bucket-1257994648.cos.ap-chengdu.myqcloud.com/' + blog_name + '/' + blog_name + '_' + str(i) + '.' + "png" + ')', lines[x], count=1)
            try:
                urllib.request.urlretrieve(l.group(1)+'//'+l.group(3), 'D:/临时/'+blog_name+'_'+str(i) + '.'+'png')
            except UnicodeEncodeError:
                print("编码异常")

            # 读取图片字节流
            fp = open("D:/临时/"+blog_name+'_'+str(i) + '.'+'png', 'rb')
            client.put_object(
                Bucket='pic-bucket-1257994648',  # Bucket由bucketname-appid组成
                Body=fp,
                Key=blog_name + '/' + blog_name + '_' + str(i) + '.' + "png",
                StorageClass='STANDARD',
                ContentType='text/html; charset=utf-8'
            )
            i = i + 1

    # 写入博客
    with open(blog_url, encoding='utf-8', mode='w') as  f:
        f.writelines(lines)
    print('完成')

blog_process('C:\\Users\\zzp\\OneDrive - stu.xjtu.edu.cn\\文档\\blog\\source\\_posts\\GIF_图片格式详解.md')