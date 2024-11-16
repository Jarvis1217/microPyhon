import time
import network
from microdot import Microdot

# 连接wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = '<WIFI_NAME>'
password = '<WIFI_PASS>'
wlan.connect(ssid, password)

while not wlan.isconnected():
    print('正在尝试连接...')
    time.sleep(1)
print('连接成功，网络配置：', wlan.ifconfig())

# microDot
app = Microdot()

@app.route('/')
def index(request):
    return 'Hello, Microdot on ESP32!'

app.run(host='0.0.0.0', port=5000)