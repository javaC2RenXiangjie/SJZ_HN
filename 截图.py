from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import mss
import time

monitor = {'left': 2027, 'top':592, 'width':129, 'height':27}

with mss.mss() as sct:
    time.sleep(2)

    # 获取指定区域的截图
    screenshot = sct.grab(monitor)

    # 保存截图
    mss.tools.to_png(screenshot.rgb, screenshot.size, output='region_screenshot.png')
