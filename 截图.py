from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import mss
import time

monitor = {'left': 1088, 'top':592, 'width':129, 'height':29}

with mss.mss() as sct:
    time.sleep(3)

    # 获取指定区域的截图
    screenshot = sct.grab(monitor)

    # 保存截图
    mss.tools.to_png(screenshot.rgb, screenshot.size, output='region_screenshot.png')
