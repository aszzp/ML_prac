from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chromePath = r'P:\APP\chromedriver\chromedriver.exe'
wd = webdriver.Chrome(executable_path= chromePath)
wd.get('http://192.168.31.1/cgi-bin/luci/web')
print('before login')
# 初始登陆界面
wd.find_element_by_id('password').send_keys('zzp888888')
wd.find_element_by_id('btnRtSubmit').click()
# 进入拨号界面
wd.get('http://192.168.31.1/cgi-bin/luci/;stok=cf58d8d495a75a8bfbe0cc20d600e3bd/web/setting/wan')

e_con = WebDriverWait(wd, 5, 0.2).until(
                      EC.presence_of_element_located((By.ID, "pppoeStop")))
e_con.click()
e_user = WebDriverWait(wd, 5, 0.2).until(
                      EC.presence_of_element_located((By.NAME, "pppoeName")))
e_psw = WebDriverWait(wd, 5, 0.2).until(
                      EC.presence_of_element_located((By.NAME, "pppoePwd")))
user_name = e_user.get_property('value')
e_user.clear()
e_psw.clear()
# 输入账号密码
if 'liaodong2018@lt'== user_name:
    e_user.send_keys('chen_liu528@yd')
    e_psw.send_keys('937941')
else:
    e_user.send_keys('liaodong2018@lt')
    e_psw.send_keys('171467')
e_psw.click()
wd.find_element_by_tag_name('button').click()
try:
    WebDriverWait(wd, 3, 0.2).until(
                      EC.presence_of_element_located((By.ID, "pppoeStop")))
except:
    e_start = WebDriverWait(wd, 3, 0.2).until(
        EC.presence_of_element_located((By.ID, "pppoeStart")))
    e_start.click()
print('over')
wd.close()