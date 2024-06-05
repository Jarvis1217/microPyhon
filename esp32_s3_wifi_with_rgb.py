import network
from machine import Pin
import neopixel
import time

# WiFi网络名称和密码
target_ssid = 'WIFI_NAME'
password = 'WIFI_PASSWD'

# RGB初始化
pin_num = 48
num_leds = 1
brightness = 0.01
np = neopixel.NeoPixel(Pin(pin_num), num_leds)

# 初始化WiFi模块
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# 红灯等待连接WiFi
np[0] = (int(255 * brightness), 0, 0)
np.write()

# 连接到WiFi网络
print(f'Connecting to {target_ssid}...')
wlan.connect(target_ssid, password)

# 等待连接成功
while not wlan.isconnected():
    print(f'Waiting for connection...{target_ssid}')
    time.sleep(1)

# 绿灯提示WIFI连接成功
np[0] = (0, int(255 * brightness), 0)
np.write()

print('Connected to WiFi')
print('Network config:', wlan.ifconfig())

# 关闭WiFi模块
wlan.active(False)
