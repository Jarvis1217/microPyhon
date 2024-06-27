from machine import UART, Pin, I2C
import time
from mpu6050 import MPU6050

# 初始化UART
uart = UART(1, tx=9, rx=8, baudrate=115200)

# 初始化MPU6050传感器
i2c_mpu = I2C(0, scl=Pin(5), sda=Pin(4))
mpu = MPU6050(i2c_mpu)

# 定义串口屏幕的基本指令
def uart_send(cmd):
    uart.write(cmd)
    time.sleep_ms(35)

# 清屏函数
def clear_screen(color=0):
    uart_send("CLR({});\r\n".format(color))

# 画填充圆函数
def draw_filled_circle(x, y, radius, color):
    uart_send("CIRF({},{},{},{});\r\n".format(x, y, radius, color))
    
# 初始化小球位置和速度
ball_x = 64
ball_y = 64
speed_x = 0
speed_y = 0

# 重力加速度
g = 9.81

# 时间间隔
dt = 0.1

# 游戏状态
game_over = False

uart_send("DIR(1);\r\n")

# 主循环
while True:
    
    # 清屏
    clear_screen()

    if game_over:
        uart_send("DC16(30,30,'Game Over!',15);\r\n")
        time.sleep(2)
        ball_x = 64
        ball_y = 64
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
    ball_x += int(speed_x * dt + 0.5 * acc_x * dt ** 2)
    ball_y += int(speed_y * dt + 0.5 * acc_y * dt ** 2)

    # 边界检测
    if ball_x < 0 or ball_x >= 128 or ball_y < 0 or ball_y >= 128:
        game_over = True
    else:
        draw_filled_circle(ball_x, ball_y, 5, 1)

    time.sleep(dt)