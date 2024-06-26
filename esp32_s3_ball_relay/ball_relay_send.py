from machine import I2C, Pin
import ssd1306
from mpu6050 import MPU6050
import network
import espnow
import time

# 获取本地MAC地址
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
mac = wlan.config('mac')
print('本地MAC地址:', ':'.join('%02x' % b for b in mac))

# 初始化 ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# 添加接收端MAC地址
peer_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF'
esp.add_peer(peer_mac)

# 初始化I2C
i2c_oled = I2C(0, scl=Pin(35), sda=Pin(36))
i2c_mpu = I2C(1, scl=Pin(5), sda=Pin(6))

# 初始化OLED显示屏
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

# 初始化MPU6050传感器
mpu = MPU6050(i2c_mpu)

# 定义小球的初始位置
ball_x = 0
ball_y = oled_height // 2

# 定义小球的初始速度
speed_x = 0
speed_y = 0

# 定义重力加速度
g = 9.81  # m/s^2

# 定义时间间隔
dt = 0.1  # s

# 定义一个函数来绘制圆形
def draw_circle(oled, x0, y0, radius, color):
    for y in range(-radius, radius+1):
        for x in range(-radius, radius+1):
            if x*x + y*y <= radius*radius:
                oled.pixel(x0 + x, y0 + y, color)

# 主循环
while True:
    # 清屏
    oled.fill(0)

    flag_x, flag_y = True, True

    # 获取MPU6050的roll和pitch角度值
    roll, pitch = mpu.get_angle()

    if ball_x <= 0 and roll < 0:
        flag_x = False
    
    if (ball_y <= 0 and pitch < 0) or (ball_y >= oled_height and pitch > 0):
        flag_y = False

    if flag_x:
        acc_x = g * roll
        speed_x += acc_x * dt
        ball_x += int(speed_x * dt + 0.5 * acc_x * dt**2)

    if flag_y:
        acc_y = g * pitch
        speed_y += acc_y * dt
        ball_y += int(speed_y * dt + 0.5 * acc_y * dt**2)

    # 边缘检测
    if ball_x >= oled_width:

        if ball_y < 0:
            ball_y = 0
        elif ball_y >= oled_height:
            ball_y = oled_height

        esp.send(peer_mac, str(ball_y))
        oled.fill(0)
        oled.show()
        break
    elif ball_x < 0:
        ball_x = 0
    
    if ball_y < 0:
        ball_y = 0
    elif ball_y >= oled_height:
        ball_y = oled_height
    
    draw_circle(oled, ball_x, ball_y, 5, 1)

    # 显示更新后的屏幕
    oled.show()

    # 短暂延迟以降低刷新频率
    time.sleep(dt)
