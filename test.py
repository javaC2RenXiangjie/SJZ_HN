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

car_list = ['旅店用餐间', '总裁会议室', '雷达站无人机平台']

tab_area = {'长弓溪谷':{'x1': 452, 'y1':918, 'x2':639, 'y2':948}
              , '零号大坝':{'x1': 452, 'y1':971, 'x2':639, 'y2':1008}
              , '航天基地':{'x1': 452, 'y1':1033, 'x2':639, 'y2':1062}
              , '巴克什':{'x1': 452, 'y1':1100, 'x2':639, 'y2':1134}
            }

tab_car_mp = {'酒店国王房':'长弓溪谷', '雷达站无人机平台':'长弓溪谷'
            , '东楼经理室':'零号大坝', '变电站技术室':'零号大坝'
            , '总裁会客厅':'航天基地', '蓝室核心':'航天基地', '黑室服务器室':'航天基地'
            , '总裁会议室':'巴克什', '地下金库储藏间':'巴克什', '旅店用餐间':'巴克什', '博物馆展厅套间':'巴克什', '老浴场贵宾室':'巴克什'
            }

new_list = []
for c_n in car_list:
    if tab_car_mp[c_n] not in new_list:
        new_list.append(4)

# 卡购买价格
price_map = {'总裁会客厅': 5500000, '东楼经理室': 3500000, '黑室服务器室':2900000, '蓝室核心':2800000, '酒店国王房':3600000, '雷达站无人机平台':2800000, '变电站技术室':2400000, '地下金库储藏间':2600000
    , '总裁会议室':3000000, '旅店用餐间':1800000, '博物馆展厅套间':1400000, '老浴场贵宾室':1900000}

screenshot_area = {'总裁会客厅':{'left': 1086, 'top':436, 'width':131, 'height':27}
                , '黑室服务器室':{'left': 2027, 'top':436, 'width':129, 'height':27}
                , '蓝室核心':{'left': 1088, 'top':592, 'width':129, 'height':29}
                , '东楼经理室':{'left': 1086, 'top':436, 'width':131, 'height':27}
                , '酒店国王房':{'left': 1086, 'top':436, 'width':131, 'height':27}
                , '雷达站无人机平台':{'left': 1552, 'top':436, 'width':129, 'height':27}
                , '变电站技术室':{'left': 1552, 'top':436, 'width':129, 'height':27}
                , '地下金库储藏间':{'left': 1086, 'top':436, 'width':131, 'height':27}
                , '总裁会议室':{'left': 1552, 'top':436, 'width':129, 'height':27}
                , '旅店用餐间':{'left': 2027, 'top':436, 'width':129, 'height':27}
                , '博物馆展厅套间':{'left': 1552, 'top':592, 'width':129, 'height':27}
                , '老浴场贵宾室':{'left': 2027, 'top':592, 'width':129, 'height':27}
                }

click_area = {'总裁会客厅': {'x1': 766, 'y1':323, 'x2':879, 'y2':335}
              , '黑室服务器室': {'x1': 1710, 'y1':333, 'x2':1785, 'y2':337}
              , '蓝室核心': {'x1': 770, 'y1':484, 'x2':534, 'y2':496}
              , '东楼经理室': {'x1': 766, 'y1':323, 'x2':879, 'y2':335}
              , '酒店国王房': {'x1': 766, 'y1':323, 'x2':879, 'y2':335}
              , '雷达站无人机平台': {'x1': 1233, 'y1':323, 'x2':1315, 'y2':337}
              , '变电站技术室': {'x1': 1233, 'y1':323, 'x2':1315, 'y2':337}
              , '地下金库储藏间': {'x1': 766, 'y1':323, 'x2':879, 'y2':335}
              , '总裁会议室': {'x1': 1233, 'y1':323, 'x2':1315, 'y2':337}
              , '旅店用餐间': {'x1': 1710, 'y1':333, 'x2':1785, 'y2':337}
              , '博物馆展厅套间': {'x1': 1233, 'y1':484, 'x2':1351, 'y2':495}
              , '老浴场贵宾室': {'x1': 1710, 'y1':484, 'x2':1801, 'y2':491}
              }

price_check_area = {'left': 588, 'top':328, 'width':160, 'height':34}

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

def getAreaPrice(left= None, top=None, width=None, height=None):
    with mss.mss() as sct:
        time.sleep(0.1)
        # 获取指定区域的截图
        screenshot = sct.grab({'left': left, 'top':top, 'width':width, 'height':height})

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

def move_mouse_naturally(start_x, start_y, end_x, end_y, duration=0.05):
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



while len(car_list) != 0:
    print(car_list)
    time.sleep(0.1)
    if len(car_list) == 0:
        break

    tab_list = []
    for c_n in car_list:
        if tab_car_mp[c_n] not in tab_list:
            tab_list.append(tab_car_mp[c_n])
    if len(tab_list) == 1:
        if tab_list[0] != '长弓溪谷':
            tab_list.append('长弓溪谷')
        else:
            tab_list.append('航天基地')

    for tab in tab_list:
        start_x, start_y = pyautogui.position()  # 获取当前鼠标位置
        log = random.randint(tab_area[tab]['x1'], tab_area[tab]['x2'])
        lat = random.randint(tab_area[tab]['y1'], tab_area[tab]['y2'])
        move_mouse_naturally(start_x, start_y, log, lat, duration=0.05)
        # 点击进入卡片列表
        pyautogui.click(log, lat, button='left')

        # 先逐个判断需要购买卡的价格
        for car_name in car_list:
            if tab_car_mp[car_name] != tab:
                continue
            try:
                current_price = float(getAreaPrice(screenshot_area[car_name]['left'], screenshot_area[car_name]['top'], screenshot_area[car_name]['width'], screenshot_area[car_name]['height']))
            except:
                continue
            if current_price <= price_map[car_name]:
                start_x, start_y = pyautogui.position()  # 获取当前鼠标位置
                # 生成终点范围内随机坐标
                log = random.randint(click_area[car_name]['x1'], click_area[car_name]['x2'])
                lat = random.randint(click_area[car_name]['y1'], click_area[car_name]['y2'])
                move_mouse_naturally(start_x, start_y, log, lat, duration=0.05)
                # 点击进入购买界面
                pyautogui.click(log, lat, button='left')

                # 再截图一下价格，保证价格没错
                try:
                    check_price = float(getAreaPrice(price_check_area['left'], price_check_area['top'], price_check_area['width'], price_check_area['height']))
                except:
                    continue
                if check_price > price_map[car_name]:
                    keyboard.press_and_release('esc')
                    continue

                # 鼠标移动至购买按钮范围，并点击
                move_mouse_naturally(log, lat, 2025, 1100, duration=0.1)
                pyautogui.click(2025, 1100, button='left')
                print('{}---{}---{}---{}'.format('购买成功', car_name, datetime.datetime.now(), current_price))

                # 从待买列表删除已买卡片
                car_list.remove(car_name)
                keyboard.press_and_release('esc')
                move_mouse_naturally(log, lat, 1430, 200, duration=0.05)
                continue

            print('{}---{}---{}---{}'.format('正在观察', car_name, datetime.datetime.now(), current_price))






