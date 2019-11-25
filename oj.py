# oj


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup as bf
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
from io import BytesIO
import matplotlib.image as mpimg
import re
import pytesseract
from selenium import webdriver
from PIL import Image, ImageEnhance
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import cv2
# import tesserocr


driver = None


def binarizing(img):
    """传入image对象进行灰度、二值处理"""
    img = img.convert("L") # 转灰度
    img = img.point(lambda x: 255 if x > 128 else 0)
    # pixdata = img.load()
    # w, h = img.size
    # # 遍历所有像素，大于阈值的为黑色
    # for y in range(h):
    #     for x in range(w):
    #         if pixdata[x, y] < threshold:
    #             pixdata[x, y] = 0
    #         else:
    #             pixdata[x, y] = 255
    return img


def depoint(img):
    """传入二值化后的图片进行降噪"""
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h-1):
        for x in range(1, w-1):
            count = 0
            if pixdata[x, y-1] > 245:#上
                count = count + 1
            if pixdata[x, y+1] > 245:#下
                count = count + 1
            if pixdata[x-1, y] > 245:#左
                count = count + 1
            if pixdata[x+1, y] > 245:#右
                count = count + 1
            if pixdata[x-1, y-1] > 245:#左上
                count = count + 1
            if pixdata[x-1, y+1] > 245:#左下
                count = count + 1
            if pixdata[x+1, y-1] > 245:#右上
                count = count + 1
            if pixdata[x+1, y+1] > 245:#右下
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return img


def get_vcode():
    global driver
    # 浏览器页面截屏
    screenImg = "vcode.png"
    driver.get_screenshot_as_file(screenImg)
    # 定位验证码位置及大小
    elem = driver.find_elements_by_tag_name("img")[2]
    location = elem.location
    size = elem.size
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    # # 从文件读取截图，截取验证码位置再次保存
    img = Image.open(screenImg).crop((left, top, right, bottom))
    img = binarizing(img)
    img = depoint(img)
    img.save(screenImg)
    return img


def login(usr):
    global driver
    print("user_id:", usr["id"])
    driver = webdriver.Chrome(r'C:\Users\0ng\Documents\chromedriver.exe')

    driver.get("http://172.31.221.14/")
    driver.fullscreen_window()
    WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_tag_name("a")[5]).click()
    success = False
    # num = 0
    while not success:
        img = get_vcode()
        code = pytesseract.image_to_string(img, config="-psm 7")
        # # 打印识别的验证码

        b = ''
        for i in code.strip():
            pattern = re.compile(r'[0-9]')
            m = pattern.search(i)
            if m != None:
                b += i
        code = b
        # print(code)

        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_name("user_id")).clear()
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_name("user_id")).send_keys(usr["id"])
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_name("password")).clear()
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_name("password")).send_keys(usr["pwd"])
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_name("vcode")).clear()
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_name("vcode")).send_keys(code)
        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_name('submit')).click()
        try:
            alert = driver.switch_to.alert
            print("Wrong Answer")
            alert.accept()
            time.sleep(0.05)
        except:
            success = True
            print("Accept")
        # driver.find_element_by_class_name('red').click()
        # ls = driver.find_elements_by_tag_name("td")
        # for i in ls:
        #     if str(i.text).find("肖志娇") != -1:
        #         i.click()
        #         break
        # driver.find_elements_by_tag_name("a")[12].click()
        #
        # driver.find_elements_by_tag_name("a")[6].click()
        # with open("output.txt", "r") as f:
        #     code = f.read()
        # driver.find_element_by_id("textarea").click()
        # driver.find_element_by_id("textarea").send_keys(Keys.CONTROL, "v")

# login({
#         "id": "2018104021",
#         "pwd": "123456"
#     })
