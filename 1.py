from playwright.sync_api import Playwright, sync_playwright
from sys import exit
from random import randint
import json,logging,requests
from sys import platform
from time import sleep,localtime,strftime
url=""
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
key="3877cb783605f80c687eccadd138873c"
def run(playwright: Playwright,name,passwd) -> None:
    if platform=="linux":
        browser = playwright.chromium.launch(headless=True)
    elif platform=="darwin":
        browser = playwright.chromium.launch(channel="msedge",headless=True)
    else:
        print("系统支持有误，请检查")
        exit(1)
    context = browser.new_context()
    page = context.new_page()
    try:
        global url
        page.goto(url)
        sleep(0.5)
        page.fill("[placeholder=\"账号 Username\"]", name)
        page.fill("[placeholder=\"密码 Password\"]", passwd)
        page.click("text=登 录")
        sleep(1.5)
        if page.is_visible("text=账户不存在。"):
            logging.info("账户名有误")
            return False
        if page.is_visible("text=登 录"):
            logging.info("登录失败，可能是密码有误")
            return False
        c= randint(0, 5)
        page.fill("input[name=\"tw\"]", "36."+str(c))

        logging.info(name+"开始填报，体温"+"36."+str(c))
        page.click("button:has-text(\"提交\")")
        sleep(0.5)
        if page.is_visible("text=健康填报成功"):
            page.click("text=确定")
            logging.info(name+"成功！")
            context.close()
            browser.close()
            return True
        else:
            logging.info('填报网站时出错')
            return False
    except BaseException as e:
        logging.info(e)
        return False
def loaddata():
    data=json.load(open('data.json'))
    global url 
    url=data['url']
    return data['data']
    pass
def report(qq):
    qqurl="https://qmsg.zendee.cn/send/"+key+"/?msg=体温填报失败！请手动填报qq="+qq
    res=requests.get(qqurl)
    pass


def func(data):
    i = 0
    with sync_playwright() as playwright:
        for user in data:
            print(f"正在处理第{i}个")
            i=i+1
            logging.info(user)
            if run(playwright,user["name"],user["passwd"]):
                pass
            else:
                logging.info(user["name"]+"填报失败，半分钟后重试")
                return 1
    return 0
    pass
if __name__ == "__main__":
    data=loaddata()
    wait=[10,60,300,600]
    for i in range(4):
        if func(data)==0:
            exit(0)
        else:
            sleep(wait[i])
    report("1246659083")
    exit(-1)

