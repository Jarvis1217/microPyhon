import time
import network
import ntptime
from machine import Pin, I2C, RTC
from ssd1306 import SSD1306_I2C

i2c = I2C(0, scl=Pin(25), sda=Pin(26))
oled = SSD1306_I2C(128, 64, i2c)

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

ssid, passwd = 'WIFI_NAME', 'WIFI_PASS'
connect_wifi(ssid, passwd)

set_time()
 
while True:
    cur_time = RTC().datetime()
    
    oled.fill(0)
    oled.text(f'{cur_time[4]:02}:{cur_time[5]:02}:{cur_time[6]:02}', 28, 15, 1)
    oled.text(f'{cur_time[0]}/{cur_time[1]}/{cur_time[2]}', 25, 30, 1)
    oled.show()
    
    time.sleep(1)
