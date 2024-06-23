import network
import ntptime
import utime
from machine import Pin, I2C
import ssd1306

# 配置WiFi连接
SSID = 'WIFI_NAME'
PASSWORD = 'WIFI_PASSWD'

# 初始化I2C和OLED
i2c = I2C(0, scl=Pin(6), sda=Pin(7))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print('network config:', wlan.ifconfig())

# 连接WiFi
connect_wifi(SSID, PASSWORD)

# 设置时区偏移（UTC+8）
TIMEZONE_OFFSET = 8 * 3600

# 获取并校准网络时间
def set_time():
    try:
        ntptime.host = "time.windows.com"
        ntptime.settime()
    except Exception as e:
        print("Error setting time: ", e)
        return None

# 设置一次时间        
set_time()

def format_date(t):
    return "{:04}-{:02}-{:02}".format(t[0], t[1], t[2],)        

def format_time(t):
    return "{:02}:{:02}:{:02}".format(t[3], t[4], t[5])

# 主循环，每秒更新一次时间显示
while True:
    current_time = utime.localtime(utime.time() + TIMEZONE_OFFSET)
    oled.fill(0)
    oled.text(format_date(current_time), 0, 10)
    oled.text(format_time(current_time), 0, 20)
    oled.text("microPython",0, 30)
    oled.text("with ESP32",0, 40)
    oled.text("By Jerry.L",0, 50)
    oled.show()
