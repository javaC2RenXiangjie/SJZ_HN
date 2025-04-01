import mss
import cv2
import numpy as np
import pytesseract
import keyboard
import pyautogui
import time

# 设置截图区域（根据实际界面调整）
monitor = {
    "top": 100,
    "left": 100,
    "width": 400,
    "height": 400
}

def capture_price_area():
    """捕获价格区域的截图"""
    with mss.mss() as sct:
        img = sct.grab(monitor)
        img_array = np.array(img)
        return img_array

def extract_price(img):
    """从截图中提取价格信息"""
    # 转换为灰度图像
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用 OCR 提取文本
    text = pytesseract.image_to_string(img)
    # 提取价格（假设价格格式为数字）
    try:
        price = int(''.join(filter(str.isdigit, text)))
        return price
    except:
        return None

def main():
    # print("按 Alt+F 刷新价格")
    # while True:
        # 监听 Alt+F 键
    # if keyboard.is_pressed('alt+f'):
    #     # 捕获价格区域
    img = capture_price_area()
    # 提取价格
    price = extract_price(img)
    if price is not None:
        print(f"当前价格：{price}")
        # 判断价格是否低于 200W
        if price < 2000000:
            # 模拟点击购买键
            # pyautogui.click(x=购买键_x, y=购买键_y)  # 替换为实际购买键的坐标
            print("已点击购买")
    time.sleep(0.5)  # 避免重复触发




if __name__ == "__main__":
    main()