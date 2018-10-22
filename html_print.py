import requests
import pdfkit
from bs4 import BeautifulSoup
import time


def url_to_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}
    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.content, 'html5lib')
    return soup


def get_menu():
    soup = url_to_soup('https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000')
    #由于有4个标签的class属性名都是“uk。。。”，所以返回一个列表，所以可以指定其中第四个作为返回值
    menu_tag = soup.find_all(class_='uk-nav uk-nav-side')[3]
    urls = []
    # print(menu_tag)
    tags = menu_tag.find_all('a')

    for tag in tags:
        #有的tag是空值，会抛出异常
        try:
            url = 'https://www.liaoxuefeng.com' + tag['href']
            urls.append(url)
        except AttributeError:
            pass
    return urls


def htmls_to_pdf(htmls, file_name):
    """
    把所有html文件转换成pdf文件，指定以Unicode编码方式储存
    """
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')],
        'outline-depth': 10,
    }
    pdfkit.from_file(htmls, file_name, options=options)


def url_to_html(url, address_filename):
    soup = url_to_soup(url)
    body = soup.find_all(class_='x-wiki-content x-main-content')
    htm = str(body)
    print(type(htm))
    #由于网页的编码方式是utf-8.也准备以相同编码保存PDF。所以此处以Unicode编码新建一个html文档，写入内容将按照unico编码存储。这里发现一个问题，生成的html文件用浏览器打开乱码，通过开发者工具发现，浏览器是以gbk32方式打开的。如果用记事本打开就一切正常了。
    with open(address_filename, 'w', encoding='UTF_8') as f:
        f.write(htm)


def main():
    urls = get_menu()
    file_count = 0
    #htmls中储存有所有html文件的绝对路径
    htmls = []
    for url in urls:
        address_filename = r'C:\Users\zzp\Documents\pdf\pdf'+str(file_count)+'.html'
        url_to_html(url, address_filename)
        htmls.append(address_filename)
        file_count += 1
        time.sleep(15)
    #输入所有html文件的绝对路径，指定输出
    htmls_to_pdf(htmls, r"C:\Users\zzp\Documents\pdf\b.pdf")


main()
