from playwright.sync_api import Playwright, sync_playwright
import pytesseract
from PIL import Image
from sys import exit
from random import randint
import json, logging, requests
from sys import platform
from time import sleep, localtime, strftime

Alldata = {}
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

def fillcode(page):
    c=page.locator("//html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[4]/img")
    s=c.screenshot(path="test.jpg")
    code1=getcode("./test.jpg")
    print(f"获取验证码识别为{code1}")
    page.fill("//html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[4]/input", code1)
    pass
def run(playwright: Playwright, name, passwd) -> None:
    if platform == "linux":
        browser = playwright.chromium.launch(headless=True)
    elif platform == "darwin":
        browser = playwright.chromium.launch(channel="msedge", headless=False)
    elif platform == "win32":
        browser = playwright.chromium.launch(channel="msedge", headless=True)
    else:
        print("系统支持有误，请检查")
        exit(1)
    context = browser.new_context()
    page = context.new_page()
    try:
        global Alldata
        page.goto(Alldata["url"])
        sleep(0.5)
        page.fill("[placeholder=\"账号 Username\"]", name)
        page.fill("[placeholder=\"密码 Password\"]", passwd)
        fillcode(page)
        page.click("text=登 录")
        sleep(40)
        sleep(1.5)
        if page.is_visible("text=账户不存在。"):
            logging.info("账户名有误")
            return False
        if page.is_visible("text=登 录"):
            logging.info("登录失败，可能是密码有误")
            return False
        c = randint(0, 5)
        page.wait_for_timeout(6000)
        #获取用户名
        name_path = '//html/body/div/div/div/div/div[1]/div[2]/div/form/div[6]/div[1]/div/div[2]/div/div/span'
        uname = page.text_content(name_path)
        if uname == "":
            logging.info("获取姓名失败，可能是网络问题")
        page.fill("input[name=\"tw\"]", "36." + str(c))

        logging.info(name + uname + "开始填报，体温" + "36." + str(c))
        page.click("button:has-text(\"提交\")")
        sleep(0.5)
        if page.is_visible("text=健康填报成功"):
            page.click("text=确定")
            logging.info(name + "成功！")
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
    global Alldata
    Alldata = json.load(open('data.json'))
    #check data
    if Alldata['url'] == '':
        raise Exception("url为空！请检查", Alldata['url'])
    if (Alldata['token'] == '') | (Alldata['qq'] == ''):
        print("token为空或者qq为空！将无法报告错误信息")


def report(qq):
    qqurl = "https://qmsg.zendee.cn/send/" + Alldata[
        'key'] + "?msg=体温填报失败！请手动填报qq=" + qq
    res = requests.get(qqurl)
    pass


def func(data):
    i = 1
    with sync_playwright() as playwright:
        for user in data:
            wait_time = randint(0, 300)
            print(f"正在处理第{i}个，总共{len(data)}个。并等待{wait_time}秒后提交下一个")
            i = i + 1
            logging.info(user)
            if run(playwright, user["name"], user["passwd"]):
                pass
            else:
                logging.info(user["name"] + "填报失败，半分钟后重试")
                return 1
    return 0
    pass


def getcode(dir):
    im = Image.open(dir)
    #进行置灰处理
    im = im.convert('L')
    #这个是二值化阈值
    threshold = 150
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    #通过表格转换成二进制图片，1的作用是白色，0就是黑色
    im = im.point(table, "1")
    im.show()
    im = im.resize((120, 40))
    return pytesseract.image_to_string(im)


if __name__ == "__main__":
    waittime = randint(0, 1200)
    loaddata()
    wait = [10, 60, 300, 600]
    for i in range(4):
        if func(Alldata['data']) == 0:
            exit(0)
        else:
            sleep(wait[i])
    report(Alldata['qq'])
    raise Exception("失败！！！！！")
