# -*- coding: utf-8 -*-
'''
23/8/5
authur:ding
主要内容(主要都是jquery和js)
1、针对ie11的爬取信息(任何浏览器都行，把ie改了就行)
2、登录
3、单选框、多选框
4、输入框
5、文件下载、另存为(不能息屏，目前不知道息屏怎么处理)
6、遇到提示框
7、你可能会遇到当前元素内有url情况，直接拿到url，打开新的页面再定位元素
'''
from selenium import webdriver  # 导入webdriver包
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.ie.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import win32api,win32con
import autoit
#登录页面以学校网站为例(包含了输入框和登录的点击,多选框)
SYSTEM_URL=""
SYSTEM_USERNAME=''
SYSTEM_PASSWORD=''

#1、进入登录页面
#单选框和多选框(登录中有，只要找到框的元素点击即可)
def login(driver):
    driver.get(SYSTEM_URL)
    sleep(3)
    username = f"document.getElementById('username').value='{SYSTEM_USERNAME}'"
    driver.execute_script(username)
    password = f"document.getElementById('password').value='{SYSTEM_PASSWORD}'"
    driver.execute_script(password)
    # 记住密码是个多选框，不需要去除read_only,若遇到需要去除的，则如下所示(有的选择日期就需要，我找不到例子，我自己做的项目就有)
    reme_pass = '''$("#rememberMe").click()'''
    # '''document.getElementById("rememberMe").removeAttribute("readonly")'''
    driver.execute_script(reme_pass)
    driver.find_element_by_id("login_submit").send_keys(Keys.ENTER)

# 下载和另存为数据(以下载论文为例，随便找的网站，第一步与登录相同都是要进入当前页面)
#下载
filePath='D:\download'
def download(script_download, driver):
    # 这里判决书下载的时候，脚本会报错，但是可以执行，所以把异常吞掉让他继续跑
    try:
        driver.execute_script(script_download)
        #这里是判断是否有弹出框的一种方法
        # alert_accept=''''''
        # alert_accept1=driver.execute_script(alert_accept)
        # print(alert_accept1)
        # if  alert_accept1 == '确定':
        #点击确定
        #     alert_confirm = ''''''
        #     driver.execute_script(alert_confirm)
        #     sleep(1)
        # else:
        #     print("alert 未弹出")
    except Exception as e:
        print('下载脚本在页面调用时报异常，但可以尝试继续执行')
    sleep(5)
    print("*******************")
    win32api.keybd_event(117, 0, 0, 0)  # F6
    win32api.keybd_event(117, 0, win32con.KEYEVENTF_KEYUP, 0)  # F6
    sleep(0.5)
    win32api.keybd_event(9, 0, 0, 0)  # TAB
    win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    sleep(0.5)
    print("*******************")
    win32api.keybd_event(40, 0, 0, 0)  # DOWN
    win32api.keybd_event(40, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    sleep(0.5)
    win32api.keybd_event(65, 0, 0, 0)  # A
    win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # A
    sleep(3)
#存储文件
def save_file(file_path):
    file_path1=file_path+'/'+'1.pdf'
    autoit.control_set_text("另存为", "Edit1", file_path1)
    sleep(3)
    autoit.control_click("另存为", "Button2")
    sleep(2)
def download_file(driver):
    driver.get("https://aclanthology.org/2020.coling-main.419/")
    pdf = '''var url=$(".acl-paper-link-block").find("a").eq(0).attr("href");document.location=url;'''
    download(pdf, driver)
    save_file(filePath)



def alert_do(driver):
    # 碰到提示框(目前只处理过一种是div的)，也有几种方法，首先需要判断是否是弹出框
    result = EC.alert_is_present()(driver)
    # 第一种
    if result:
        result.accept()
    else:
        print("alert 未弹出")

    # 第二种(用js或者jquery找到确定的位置)
    alert_accept = ''''''
    alert_accept1 = driver.execute_script(alert_accept)
    print(alert_accept1)
    if alert_accept1 == '确定':
        # 点击确定
        alert_confirm = ''''''
        driver.execute_script(alert_confirm)
        sleep(1)
    else:
        print("alert 未弹出")


if __name__=='__main__':
    driver = webdriver.Ie()  # 使用ie浏览器
    login(driver)
    download_file(driver)
    alert_do(driver)
    # 定位到当前页面，有两种方式
    # 1、这一种可能不太准，因为可能你在进行当前页面的下一步的时候，页面元素还未加载出来，导致下一步报错，当然可以通过sleep时间长一点进入下一步，但是不稳定
    # driver.switch_to.window(driver.window_handles[-1])
    # # 2、较第一种稳定
    # handles = driver.window_handles
    # for handle in handles:
    #     if driver.title != "当前标签页":
    #         print(f'切换到标签页:当前标签页')
    #         driver.switch_to.window(handle)
    #     else:
    #         break

    #遇到iframe问题(js和jquery两种写法)，要找到iframe一共有多少个
    #第一种
    # script_to_document = '''var url=$("iframe").eq(1).attr("src");document.location=url'''
    # # 第二种(自己找)
    # script_set = f'$("#dhxMainCont").find("iframe").eq(0)[0].contentWindow.document.getElementById("xh").value=""'
    # 关闭当前窗口
    # driver.close()
    # 关闭进程
    # driver.quit()




