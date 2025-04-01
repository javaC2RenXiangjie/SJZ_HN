import datetime
import math
import time
import random

import keyboard
import mss
import numpy as np
import pytesseract
import pygetwindow as gw
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os
import cv2
import pyautogui
import win32api
import win32con

# 设置 Tesseract 可执行文件路径（如果未添加到环境变量中）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 设置 TESSDATA_PREFIX 环境变量
os.environ["TESSDATA_PREFIX"] = r'C:\Program Files\Tesseract-OCR\tessdata'

# 定义截屏区域
# left = 1832
# top = 1030
# width = 259
# height = 34

left = 581
top = 324
width = 140
height = 39
monitor = {"top": top, "left": left, "width": width, "height": height}
price_map = {'总裁会客厅': 5500000}


def imgClean(img):
    # 转换为 OpenCV 图像
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 图像预处理
    # 转为灰度图像
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # 放大图像
    upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # 二值化处理
    _, thresh = cv2.threshold(upscaled, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 形态学操作（膨胀和侵蚀）
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    return eroded

def getTextFromImg(eroded):
    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    # 使用 pytesseract 提取文字
    text = pytesseract.image_to_string(Image.fromarray(eroded), config=config)  # 指定语言为简体中文

    return text

def getAreaPrice():
    with mss.mss() as sct:
        time.sleep(0.1)
        # 获取指定区域的截图
        screenshot = sct.grab(monitor)
        # # 保存截图
        # mss.tools.to_png(screenshot.rgb, screenshot.size, output='region_screenshot.png')

        # 将截图转换为 PIL 图像
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        # 图片清晰，提高识别准确率
        eroded = imgClean(img)

        # 文字识别并提取
        text = getTextFromImg(eroded)
        return text

def press_esc():
    # 模拟按下 ESC 键
    win32api.keybd_event(win32con.VK_ESCAPE, 0, 0, 0)  # 按下
    win32api.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_KEYUP, 0)

def move_mouse_naturally(start_x, start_y, end_x, end_y, duration=0.1):
    """
    模拟自然的鼠标移动路径

    :param start_x: 起始 x 坐标
    :param start_y: 起始 y 坐标
    :param end_x: 目标 x 坐标
    :param end_y: 目标 y 坐标
    :param duration: 移动时间（秒）
    """
    # 计算距离
    distance = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
    # 计算步数
    steps = max(1, int(distance / 10))  # 每 10 像素一步
    # 计算每一步的增量
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    # 计算每一步的时间间隔
    interval = duration / steps

    # 平滑移动
    for i in range(steps):
        # 添加随机偏移
        random_offset_x = random.uniform(-5, 5)
        random_offset_y = random.uniform(-5, 5)
        current_x = start_x + dx * i + random_offset_x
        current_y = start_y + dy * i + random_offset_y
        pyautogui.moveTo(current_x, current_y, _pause=False)
        time.sleep(interval)

windows = gw.getWindowsWithTitle('三角洲行动  ')
window = windows[0]
# 激活窗口
window.activate()
print('# 窗口激活成功')
time.sleep(5)

while True:
    start_x, start_y = pyautogui.position()  # 获取当前鼠标位置
    # 生成范围内随机坐标
    log = random.randint(766, 851)
    lat = random.randint(323, 439)
    move_mouse_naturally(start_x, start_y, log, lat, duration=0.1)
    time.sleep(0.1)
    pyautogui.click(log, lat, button='left')

    current_price = float(getAreaPrice())
    if current_price <= price_map['总裁会客厅']:
        time.sleep(0.1)
        move_mouse_naturally(log, lat, 2025, 1100, duration=0.1)
        pyautogui.click(2025, 1100, button='left')
        print('{}   {}   {}'.format('购买成功', datetime.datetime.now(), current_price))
        break

    time.sleep(0.1)
    print('{}   {}'.format(datetime.datetime.now(), current_price))
    keyboard.press_and_release('esc')





