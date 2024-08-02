import time
import network
import ntptime
import math
import neopixel
import _thread
from machine import Pin, PWM, I2C, RTC
from ssd1306 import SSD1306_I2C

i2c = I2C(0, scl=Pin(35), sda=Pin(36))
oled = SSD1306_I2C(128, 64, i2c)

# 创建PWM对象
buzzer = PWM(Pin(10))
buzzer.duty(0)

A = Pin(5, Pin.IN, Pin.PULL_DOWN)
B = Pin(6, Pin.IN, Pin.PULL_DOWN)

# 初始化
pin_num = 48
num_leds = 1
np = neopixel.NeoPixel(Pin(pin_num), num_leds)


# 连接 wifi
def connect_wifi(ssid, passwd):
    wlan = network.WLAN(network.STA_IF);
    wlan.active(True)
    wlan.connect(ssid, passwd)
    while not wlan.isconnected():
        time.sleep(0.1)
    print(f'wifi已连接: {wlan.ifconfig()}')

# 设置时间
def set_time():
    ntptime.host = "ntp.aliyun.com"
    ntptime.settime()
    cur_time = time.localtime(time.time() + 8 * 3600)
    RTC().datetime((cur_time[0], cur_time[1], cur_time[2], 0, cur_time[3], cur_time[4], cur_time[5], 0))

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

ssid, passwd = 'EDU_NET', 'admin@2024'
connect_wifi(ssid, passwd)

set_time()

# 定义七音阶的频率 (C大调: C, D, E, F, G, A, B)
tones = {
    'C': 260,
    'D': 290,
    'E': 330,
    'F': 350,
    'G': 390,
    'A': 440,
    'B': 490
}

# 欢乐颂的完整音符和时值
melody = [
    ('E', 0.5), ('E', 0.5), ('F', 0.5), ('G', 0.5),
    ('G', 0.5), ('F', 0.5), ('E', 0.5), ('D', 0.5),
    ('C', 0.5), ('C', 0.5), ('D', 0.5), ('E', 0.5),
    ('E', 0.75), ('D', 0.25), ('D', 1.0),

    ('E', 0.5), ('E', 0.5), ('F', 0.5), ('G', 0.5),
    ('G', 0.5), ('F', 0.5), ('E', 0.5), ('D', 0.5),
    ('C', 0.5), ('C', 0.5), ('D', 0.5), ('E', 0.5),
    ('D', 0.75), ('C', 0.25), ('C', 1.0),

    ('D', 0.5), ('D', 0.5), ('E', 0.5), ('C', 0.5),
    ('D', 0.5), ('E', 0.2), ('F', 0.25), ('E', 0.5), ('C', 0.5),
    ('D', 0.5), ('E', 0.2), ('F', 0.25), ('E', 0.5), ('D', 0.5),
    ('C', 0.5), ('D', 0.5), ('G', 0.5),

    ('E', 0.5), ('E', 1), ('F', 0.5), ('G', 0.5),
    ('G', 0.5), ('F', 0.5), ('E', 0.5), ('D', 0.5),
    ('C', 0.5), ('C', 0.5), ('D', 0.5), ('E', 0.5),
    ('D', 0.75), ('C', 0.25), ('C', 1.0)
]

def play_tone(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty(320)  # 设置占空比
    time.sleep(duration)
    buzzer.duty(0)    # 停止蜂鸣器

def play_melody():
    # 播放欢乐颂
    for note, duration in melody:
        if note in tones:
            play_tone(tones[note], duration)
        time.sleep(0.1)

def update_time_thread():
    while True:
        cur_time = RTC().datetime()
        
        oled.fill(0)
        oled.text(f'{cur_time[4]:02}:{cur_time[5]:02}:{cur_time[6]:02}', 28, 15, 1)
        oled.text(f'{cur_time[0]}/{cur_time[1]}/{cur_time[2]}', 25, 30, 1)
        oled.show()
        time.sleep(1)

# 独立线程更新时间
_thread.start_new_thread(update_time_thread, ())

while True: 
    if A.value() == 1:
        play_melody()
        while A.value() == 1:
            time.sleep_ms(10)

    if B.value() == 1:
        breathe_in((255, 0, 0), 2)  # 红色逐渐变亮，周期2秒
        breathe_out((255, 0, 0), 2) # 红色逐渐变暗，周期2秒

        breathe_in((0, 255, 0), 2)  # 绿色逐渐变亮，周期2秒
        breathe_out((0, 255, 0), 2) # 绿色逐渐变暗，周期2秒

        breathe_in((0, 0, 255), 2)  # 蓝色逐渐变亮，周期2秒
        breathe_out((0, 0, 255), 2) # 蓝色逐渐变暗，周期2秒
        while B.value() == 1:
            time.sleep_ms(10)
    time.sleep_ms(50)
