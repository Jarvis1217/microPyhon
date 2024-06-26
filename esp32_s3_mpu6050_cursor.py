from machine import I2C, Pin
from mpu6050 import MPU6050
from ssd1306 import SSD1306_I2C
import time
import math

# 初始化I2C
i2c_6050 = I2C(0, scl=Pin(5), sda=Pin(6))
i2c_oled = I2C(1, scl=Pin(35), sda=Pin(36))

# 初始化MPU6050传感器
mpu = MPU6050(i2c_6050)

# 初始化SSD1306 OLED显示屏
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c_oled)

# 定义一个函数计算角度
def calculate_angle(accel_data):
    x = accel_data[0]
    y = accel_data[1]
    z = accel_data[2]
    roll = math.atan2(y, z) * 57.2958
    pitch = math.atan2(-x, math.sqrt(y * y + z * z)) * 57.2958
    return roll, pitch

# 画十字和移动点的函数
def draw_cross_and_point(oled, roll, pitch):
    oled.fill(0)
    # 画十字
    oled.hline(0, oled_height // 2, oled_width, 1)
    oled.vline(oled_width // 2, 0, oled_height, 1)
    # 根据roll和pitch计算小白点的位置
    x = oled_width // 2 + int(roll)
    y = oled_height // 2 + int(pitch)
    # 确保小白点在屏幕范围内
    x = max(0, min(oled_width - 1, x))
    y = max(0, min(oled_height - 1, y))
    # 画点
    ball_radius = 3
    for i in range(-ball_radius, ball_radius + 1):
        for j in range(-ball_radius, ball_radius + 1):
            if i**2 + j**2 <= ball_radius**2:
                oled.pixel(x + i, y + j, 1)
                
    oled.show()

# 主循环，读取传感器数据并更新OLED显示
while True:
    accel_data = mpu.accel
    roll, pitch = calculate_angle(accel_data)
    draw_cross_and_point(oled, roll, pitch)
