from machine import I2C, Pin
from mpu6050 import MPU6050
import network
import socket
import time
import math

# 初始化I2C
i2c = I2C(1, scl=Pin(5), sda=Pin(6))

# 初始化MPU6050传感器
mpu = MPU6050(i2c)

# 设置WiFi为AP模式
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='esp_mouse', authmode=network.AUTH_OPEN)

while not ap.active():
    pass

print('AP模式激活, 配置信息:', ap.ifconfig())

# 定义一个函数计算角度
def calculate_angle(accel_data):
    x = accel_data[0]
    y = accel_data[1]
    z = accel_data[2]
    roll = math.atan2(y, z) * 57.2958
    pitch = math.atan2(-x, math.sqrt(y * y + z * z)) * 57.2958
    return roll, pitch

# 创建UDP套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 80))
print('UDP服务器已启动')


# 等待设备连接到WiFi
print('等待设备连接到WiFi...')
while True:
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    connected_devices = ap.status('stations')

    if connected_devices:
        print('设备已连接:', connected_devices)
        break

    time.sleep(1)

while True:
    roll, pitch = calculate_angle(mpu.accel)
    # print("Roll: {:.2f}, Pitch: {:.2f}".format(roll, pitch))
    
    response = 'stop'
   
    if pitch < -45:
        response = 'down'
    elif pitch > 45:
        response = 'up'
        
    if roll  < -45:
        response = 'left'
    elif roll > 45:
        response = 'right'
    
    try:
        udp_socket.sendto(response.encode(), ('192.168.4.2',12345))
        print(f"已发送：{response.encode()}")
    except:
        print("发送出错")
        continue
