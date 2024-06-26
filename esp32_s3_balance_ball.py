from machine import I2C, Pin
import ssd1306
from mpu6050 import MPU6050
import time

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
ball_x = oled_width // 2
ball_y = oled_height // 2

# 定义小球的初始速度
speed_x = 0
speed_y = 0

# 定义重力加速度
g = 9.81  # m/s^2

# 定义时间间隔
dt = 0.1  # s

# 定义游戏状态
game_over = False

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

    if game_over:
        oled.text("Game Over!", 30, 30)
        oled.show()
        time.sleep(2)  # 显示2秒游戏结束信息
        # 重新开始游戏
        ball_x = oled_width // 2
        ball_y = oled_height // 2
        speed_x = 0
        speed_y = 0
        game_over = False
        continue

    # 获取MPU6050的roll和pitch角度值
    roll, pitch = mpu.get_angle()

    # 计算小球在X和Y方向的加速度
    acc_x = g * roll
    acc_y = g * pitch

    # 更新小球的速度
    speed_x += acc_x * dt
    speed_y += acc_y * dt

    # 更新小球的位置
    ball_x += int(speed_x * dt + 0.5 * acc_x * dt**2)
    ball_y += int(speed_y * dt + 0.5 * acc_y * dt**2)


    # 边界检测，判断是否游戏结束
    if ball_x < 0 or ball_x >= oled_width or ball_y < 0 or ball_y >= oled_height:
        game_over = True
    else:
        # 在屏幕上画小球
        draw_circle(oled, ball_x, ball_y, 5, 1)

    # 显示更新后的屏幕
    oled.show()

    # 短暂延迟以降低刷新频率
    time.sleep(dt)
