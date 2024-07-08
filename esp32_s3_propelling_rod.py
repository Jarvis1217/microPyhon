from machine import Pin, I2C, PWM
from time import sleep
import ssd1306

# 初始化OLED
i2c = I2C(1, scl=Pin(21), sda=Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# 油门
gas_pedal = PWM(Pin(14))
gas_pedal.freq(1000)

# 刹车
braker = Pin(13, Pin.OUT, value=1)

# 换向
change_dir = Pin(16, Pin.OUT, value=1)

# 初始化按钮
select_button = Pin(18, Pin.IN, Pin.PULL_DOWN)
confirm_button = Pin(19, Pin.IN, Pin.PULL_DOWN)

# 定义变量
current_gear = 1 # 当前档位
gear_dict = {1:"1st", 2:"2nd", 3:"3rd"} # 档位显示字典

rect_xy = [(0, 26), (70, 26), (40, 46), (0, 46), (68, 46)] # 矩形框位置
rect_index = 0 # 记录当前矩形框位置

direction = 0 # 记录方向
mod = 0 # 记录模式

# 绘制主屏幕
def draw_main_frame():
    # 清屏
    oled.fill(0)

    # 标题
    oled.text('Func', 0, 10)
    oled.text(f'{gear_dict.get(current_gear)}', 95, 10)

    # 分割线
    oled.hline(0, 20, 128, 1)

    # 菜单项
    oled.text(f'Gear {current_gear}', 2, 30)
    oled.text(f'Dir {direction}', 77, 30)
    oled.text('Ready', 45, 50)

    # 矩形框
    oled.rect(rect_xy[rect_index][0], rect_xy[rect_index][1], 55, 16, 1)

    oled.show()

# 绘制行进界面
def draw_ready_frame():
    oled.fill(0)

    oled.text('Ready', 0, 10)
    oled.text(f'{gear_dict.get(current_gear)}', 80, 10)
    oled.hline(0, 20, 128, 1)

    oled.text('confirm to go', 0, 25)
    oled.text('select to stop', 0, 35)
    oled.rect(rect_xy[rect_index][0], rect_xy[rect_index][1], 55, 16, 1)
    oled.text('OK?', 10,50)
    oled.text('cancel', 70, 50)

    oled.show()

# select按钮按下时执行
def on_select_button_pressed(pin):
    n = 0
    if pin.value() == 1:  # 避免按键抖动
        global rect_index
        global mod
        if mod == 0:
            rect_index = (rect_index + 1) % 3
            draw_main_frame()
        elif mod == 1:
            rect_index = 7 - rect_index
            draw_ready_frame()
        elif mod == 11:
            gas_pedal.duty(0)
            braker.value(1)
        while pin.value() == 1:
            sleep(0.01)  # 等待按钮释放
            n += 1
            if n > 100 and confirm_button.value():
                mod = 0
                rect_index = 0
                draw_main_frame()

# confirm按钮按下时执行
def on_confirm_button_pressed(pin):
    global mod
    if pin.value() == 1:  # 避免按键抖动
        global rect_index
        
        if mod == 0:
            global current_gear
            global direction

            if rect_index == 0:  # 调整档位
                current_gear = (current_gear % 3) + 1
                draw_main_frame()

            elif rect_index == 1: # 调整方向
                change_dir.value(0)
                sleep(3)
                change_dir.value(1)

                direction = 1 - direction
                draw_main_frame()

            elif rect_index == 2: # 选择模式一
                rect_index = 3
                mod = 1
                draw_ready_frame()
        elif mod == 1:
            if rect_index == 3:
                mod = 11
                oled.fill_rect(0, 46, 128, 18, 0)
                oled.show()
            elif rect_index == 4:
                mod = 0
                rect_index = 0
                draw_main_frame()
        elif mod == 11:
            gas_pedal.duty(420 + current_gear * 200)
            braker.value(1)
        while pin.value() == 1:
            sleep(0.01)  # 等待按钮释放
            if select_button.value():
                braker.value(0)
            else:
                braker.value(1)

# 绘制主菜单
draw_main_frame()

while True:
    braker.value(1) # 保持不刹车
    gas_pedal.duty(0) # 保持无油门

    if select_button.value() == 1:
        on_select_button_pressed(select_button)

    elif confirm_button.value() == 1:
        on_confirm_button_pressed(confirm_button)

    # 设置按键中断
    # select_button.irq(trigger=Pin.IRQ_RISING, handler=on_select_button_pressed)
    # confirm_button.irq(trigger=Pin.IRQ_RISING, handler=on_confirm_button_pressed)
