from machine import Pin, I2C
from time import sleep
import ssd1306

# 初始化I2C
i2c = I2C(1, scl=Pin(6), sda=Pin(7))

# 初始化OLED显示屏
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# 初始化按钮
select_button = Pin(15, Pin.IN, Pin.PULL_DOWN)
confirm_button = Pin(5, Pin.IN, Pin.PULL_DOWN)

# 定义变量
battery = 100
current_gear = 1
direction = 0
rect_xy = [(0, 26), (73, 26), (0, 46), (73, 46), (0, 46), (68, 46)] # 矩形框四个位置
rect_index = 0 # 记录当前矩形框位置
gear_dict = {1:"1st", 2:"2nd", 3:"3rd"} # 档位显示字典
mod = 0 # 当前模式 main_frame

# 绘制主屏幕
def draw_main_frame():
    global mod
    mod = 0
    # 清屏
    oled.fill(0)

    # 标题
    oled.text('Func', 0, 10)
    oled.text(f'{gear_dict.get(current_gear)} {battery}%', 65, 10)

    # 分割线
    oled.hline(0, 20, 128, 1)

    # 菜单项
    oled.text(f'Gear {current_gear}', 2, 30)
    oled.text(f'Dir {direction}', 75, 30)
    oled.text('Mode 1', 2, 50)
    oled.text('Mode 2', 75, 50)

    # 矩形框
    oled.rect(rect_xy[rect_index][0], rect_xy[rect_index][1], 55, 16, 1)

    oled.show()

# 绘制模式一
def draw_mod1_frame():
    global mod
    mod = 1

    # 清屏
    oled.fill(0)

    oled.text('Mod1', 0, 10)
    oled.text(f'{gear_dict.get(current_gear)} {battery}%', 65, 10)
    oled.hline(0, 20, 128, 1)

    oled.text('select to go', 0, 25)
    oled.text('confirm to stop', 0, 35)
    oled.rect(rect_xy[rect_index][0], rect_xy[rect_index][1], 55, 16, 1)
    oled.text('OK?', 10,50)
    oled.text('cancel', 70, 50)

    oled.show()

# 绘制模式二
def draw_mod2_frame():
    global mod
    mod = 2

    # 清屏
    oled.fill(0)

    oled.text('Mod2', 0, 10)
    oled.text(f'{gear_dict.get(current_gear)} {battery}%', 65, 10)
    oled.hline(0, 20, 128, 1)

    oled.text('auto go', 0, 25)
    oled.text('confirm to stop', 0, 35)
    oled.rect(rect_xy[rect_index][0], rect_xy[rect_index][1], 55, 16, 1)
    oled.text('OK?', 10,50)
    oled.text('cancel', 70, 50)

    oled.show()

# select按钮按下时执行
def on_select_button_pressed(pin, mod):
    sleep(0.1)
    if pin.value() == 1:  # 避免按键抖动
        global rect_index

        if mod == 0:
            rect_index = (rect_index + 1) % 4 if rect_index < 4 else 0
            draw_main_frame()
        elif mod == 1:
            rect_index = 9 - rect_index
            draw_mod1_frame()
        elif mod == 2:
            rect_index = 9 - rect_index
            draw_mod2_frame()

        while pin.value() == 1:
            sleep(0.01)  # 等待按钮释放

# confirm按钮按下时执行
def on_confirm_button_pressed(pin, mod):
    sleep(0.1)
    if pin.value() == 1:  # 避免按键抖动
        global rect_index

        if mod == 0:
            global current_gear
            global direction

            if rect_index == 0:  # 调整档位
                current_gear = (current_gear % 3) + 1
                draw_main_frame()

            elif rect_index == 1: # 调整方向
                direction = 1 - direction
                draw_main_frame()

            elif rect_index == 2: # 选择模式一
                rect_index = 4
                draw_mod1_frame()

            elif rect_index == 3: # 选择模式二
                rect_index = 4
                draw_mod2_frame()
        elif mod == 1:
            if rect_index == 4:
                oled.fill_rect(0, 46, 128, 18, 0)
                oled.show()
            elif rect_index == 5:
                rect_index = 0
                draw_main_frame()
        elif mod == 2:
            if rect_index == 4:
                oled.fill_rect(0, 46, 128, 18, 0)
                oled.show()
            elif rect_index == 5:
                rect_index = 0
                draw_main_frame()
        
        while pin.value() == 1:
            sleep(0.01)  # 等待按钮释放

# 绘制主菜单
draw_main_frame()

# 监听按键, mod 0是main_frame
while True:
    if select_button.value() == 1:
        on_select_button_pressed(select_button, mod)

    if confirm_button.value() == 1:
        on_confirm_button_pressed(confirm_button, mod)

    # # 设置按键中断
    # select_button.irq(trigger=Pin.IRQ_RISING, handler=on_select_button_pressed)
    # confirm_button.irq(trigger=Pin.IRQ_RISING, handler=on_confirm_button_pressed)
