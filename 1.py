from playwright.sync_api import Playwright, sync_playwright
import pytesseract
from PIL import Image
from sys import exit
from random import randint
import json, logging, requests
from sys import platform,argv
from time import sleep, localtime, strftime
successflag=0
errorflag=0
Alldata = {}
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

def fillcode(page):
    c=page.locator("//html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[4]/img")
    s=c.screenshot(path="test.jpg")
    code1=getcode("./test.jpg")
    print(f"获取验证码识别为{code1}")
    page.click("//html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[4]/input")
    for i in range(4):
        sleep(0.2)
        page.keyboard.press(code1[i])
    # page.fill("//html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[4]/input", code1)
def run( name, passwd) -> None:
    with sync_playwright() as playwright:
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
        page.set_default_timeout(60000)
        try:
            global Alldata
            page.goto(Alldata["url"])
            sleep(0.5)
            page.fill("[placeholder=\"账号 Username\"]", name)
            page.fill("[placeholder=\"密码 Password\"]", passwd)
            fillcode(page)
            page.click('//*[@id="passbutton"]')
            sleep(1.5)
            if page.is_visible("text=验证码信息无效。"):
                logging.info("验证码识别出错")
                return False
            if page.is_visible("text=账户不存在。"):
                logging.info("账户名有误")
                return False
            if page.is_visible("text=登 录"):
                logging.info("登录失败，可能是密码有误")
                return False
            c = randint(0, 5)
            page.wait_for_timeout(6000)
            page.goto(Alldata["url"])
            # 获取用户名
            name_path = '//*[@id="form"]/div[6]/div[1]/div/div[2]/div/div/span'
            uname = page.text_content(name_path)
            if uname == "":
                logging.info("获取姓名失败，可能是网络问题")
            page.fill('//*[@id="form"]/div[18]/div[1]/div/div[2]/div/div/input', "36." + str(c))

            logging.info(name  + uname+"开始填报，体温" + "36." + str(c))
            page.click('//*[@id="post"]')
            sleep(0.5)
            if page.is_visible("text=健康填报成功"):
                page.click("text=确定")
                successflag+=1
                logging.info(name + "成功！",f"已经成功了{successflag}个")

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
    if len(data)==0:
        exit(0)
    global errorflag
    c=errorflag*60
    print(f"等待{c}秒后继续")
    sleep(c)
    if errorflag>=10:
        report(Alldata['qq'])
        exit(1)
    i = 0
    for j  in range(len(data)):
        user = data[0]
        wait_time = randint(0, 300)
        print(f"正在处理第{i}个，总共{len(data)}个。并等待{wait_time}秒后提交下一个")
        logging.info(user)
        if run(user["name"], user["passwd"]):
            if len(argv)>1:
                sleep(wait_time)
            i = i + 1
            del data[0]
        else:
            logging.info(user["name"] + "填报失败，半分钟后重试")
            errorflag+=1
            func(data)
            break
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
    # im.show()
    im = im.resize((120, 40))
    return pytesseract.image_to_string(im)


if __name__ == "__main__":
    if len(argv)>1:
        print(f"等待{waittime}秒")
        sleep(waittime)
    waittime = randint(0, 1200)
    loaddata()
    data=Alldata['data']
    wait = [10, 60, 120,300, 600]
    data2=func(data)
    raise Exception("失败！！！！！")
