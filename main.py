import re    # 正则表达式，用于匹配字符
from urllib import request
import requests
import time
import random
import os

# 设置日志文件路径
log_file_path = 'log.txt'

# 第一个post请求的URL
post_URL = 'http://10.10.9.9/eportal/InterFace.do?method=login'
# 第二个get请求的URL（浏览器可访问的url）
get_URL = 'http://10.10.9.9/eportal/success.jsp?userIndex=61613566393339653263613830393664323762386466623933626331356430345f35392e37392e352e395f3231313231393437&keepaliveInterval=0'
while(True):
    print("自动联网脚本开始运行...")
    # 请求校园网url
    response = request.urlopen(get_URL)
    html = response.read()
    # 获取tittle元素内容
    res = re.findall('<title>(.*)</title>', html.decode(encoding="GBK", errors="strict"))
    print('res:', res)
    title = ''
    if len(res) == 0:
        print("访问",get_URL,"失败，请检查请求地址！")
        pass
    else:
        title = res[0]
    print("title:",title)
    # 根据title元素内容判断是否处于已登录状态
    if title == '登录成功':    
        print('当前状态为：已登陆成功！')
    else:
        print('当前状态为：未登录！')
        # 设置post的请求头，浏览器点击F12，在Netword中选中post请求，点击Headers、request header面板中查看
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            #"Content-Length": "118",
            #"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "EPORTAL_COOKIE_USERNAME=21121947; EPORTAL_COOKIE_DOMAIN=false; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_NEWV=true; EPORTAL_COOKIE_PASSWORD=3a741c7f26b31a08577f3fb2513791ce42a61b0cac51363391c66fd0fae0a28f83c11566cffc0f2163c67cb24c1abf81f94d1a266033833708421b03ac6690a12be7781c31dd4d9b30be07d393d2fc0502d1e3befb260e5b3d23160cefa339339d4534abcfb234b9395216c13da8c3e4a544c3d48a297fd469882a7b995468bb; EPORTAL_AUTO_LAND=; EPORTAL_COOKIE_SERVER=shu; EPORTAL_COOKIE_SERVER_NAME=%E6%A0%A1%E5%9B%AD%E7%BD%91; EPORTAL_USER_GROUP=root; JSESSIONID=2111468185CCC266BA40D41FD0EDA8C6",
            "Host": "10.10.9.9",
            #"Origin": "http://10.10.9.9",
            "Upgrade-Insecure-Requests":"1",
            "Referer": "http://10.10.9.9/eportal/index.jsp?wlanuserip=59.79.5.9&wlanacname=BS_RG-N18012-Co&ssid=&nasip=172.18.2.52&snmpagentip=&mac=fc5cee4e37af&t=wireless-v2-plain&url=http://www.msftconnecttest.com/redirect&apmac=&nasid=BS_RG-N18012-Co&vid=914&port=40&nasportid=FortyGigabitEthernet%201/1/44.09140000:914-0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.5211 SLBChan/112",
        }
        # 设置post的请求数据，浏览器点击F12，在Netword中选中post请求，点击payload面板中查看
        data = {
            "userId": '21121947',  # 校园网账号
            "password": '3a741c7f26b31a08577f3fb2513791ce42a61b0cac51363391c66fd0fae0a28f83c11566cffc0f2163c67cb24c1abf81f94d1a266033833708421b03ac6690a12be7781c31dd4d9b30be07d393d2fc0502d1e3befb260e5b3d23160cefa339339d4534abcfb234b9395216c13da8c3e4a544c3d48a297fd469882a7b995468bb',  # 校园网密码（密文）
            "queryString": 'wlanuserip%3D59.79.5.9%26wlanacname%3DBS_RG-N18012-Co%26ssid%3D%26nasip%3D172.18.2.52%26snmpagentip%3D%26mac%3Dfc5cee4e37af%26t%3Dwireless-v2-plain%26url%3Dhttp%3A%2F%2Fwww.msftconnecttest.com%2Fredirect%26apmac%3D%26nasid%3DBS_RG-N18012-Co%26vid%3D914%26port%3D40%26nasportid%3DFortyGigabitEthernet%25201%2F1%2F44.09140000%3A914-0',
            "passwordEncrypt": 'true',
            "operatorPwd": '',
            "operatorUserId": '',
            "validcode": '',
            "service": 'shu',
        }
        # 发送post请求（设置好header和data）
        response = requests.post(post_URL, data, headers=header)
        uft_str = response.text.encode("iso-8859-1").decode('utf-8')
        print("post请求状态码{}".format(response))  # 打印状态码

        # 发送get请求，登录校园网
        schoolWebLoginURL = get_URL
        response = requests.get(schoolWebLoginURL).status_code  # 直接利用 GET 方式请求这个 URL 同时获取状态码
        print("get请求状态码{}".format(response))  # 打印状态码

    # 将print的内容写入log文件
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write("自动联网脚本开始运行...\n")
        log_file.write(f"res: {res}\n")
        log_file.write(f"title: {title}\n")
        log_file.write(f"当前状态为: {'已登陆成功' if title == '登录成功' else '未登录'}\n")
        log_file.write(f"状态码: {response}\n")

    # 检查文件大小，如果大于1KB则清空文件
    if os.path.getsize(log_file_path) > 1024:
        open(log_file_path, 'w').close()

    # 每1h左右检测一次是否成功连接
    rand = random.uniform(0, 100)
    print("休眠",int(3600.0 + rand),"s")
    time.sleep(3600.0 + rand)

