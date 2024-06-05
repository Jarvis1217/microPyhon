import network
import time

# WiFi网络名称和密码
target_ssid = 'WIFI_NAME'
password = 'WIFI_PASSWD'

# 初始化WiFi模块
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# 扫描WiFi网络
print("Scanning for WiFi networks...")
networks = wlan.scan()

# 打印扫描结果
print("WiFi networks found:")
for network in networks:
    ssid = network[0].decode('utf-8')  # 网络名称 (SSID)
    rssi = network[3]  # 信号强度 (RSSI)
    print(f"SSID: {ssid}, RSSI: {rssi}")

# 连接到WiFi网络
print(f'Connecting to {target_ssid}...')
wlan.connect(target_ssid, password)

# 等待连接成功
while not wlan.isconnected():
    print(f'Waiting for connection...{target_ssid}')
    time.sleep(1)

print('Connected to WiFi')
print('Network config:', wlan.ifconfig())

# 关闭WiFi模块
wlan.active(False)
