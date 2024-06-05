import time
import math
from machine import Pin
import neopixel

# 初始化
pin_num = 48
num_leds = 1
np = neopixel.NeoPixel(Pin(pin_num), num_leds)

# 呼吸灯函数
def breathe_in(color, duration, steps=100):
    for i in range(steps):
        brightness = 0.5 * (1 - math.cos(math.pi * i / steps))
        r = int(color[0] * brightness)
        g = int(color[1] * brightness)
        b = int(color[2] * brightness)
        np[0] = (r, g, b)
        np.write()
        time.sleep(duration / (2 * steps))

def breathe_out(color, duration, steps=100):
    for i in range(steps):
        brightness = 0.5 * (1 + math.cos(math.pi * i / steps))
        r = int(color[0] * brightness)
        g = int(color[1] * brightness)
        b = int(color[2] * brightness)
        np[0] = (r, g, b)
        np.write()
        time.sleep(duration / (2 * steps))

# 主循环
while True:
    breathe_in((255, 0, 0), 2)  # 红色逐渐变亮，周期2秒
    breathe_out((255, 0, 0), 2) # 红色逐渐变暗，周期2秒

    breathe_in((0, 255, 0), 2)  # 绿色逐渐变亮，周期2秒
    breathe_out((0, 255, 0), 2) # 绿色逐渐变暗，周期2秒

    breathe_in((0, 0, 255), 2)  # 蓝色逐渐变亮，周期2秒
    breathe_out((0, 0, 255), 2) # 蓝色逐渐变暗，周期2秒
