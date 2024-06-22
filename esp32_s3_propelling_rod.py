from machine import Pin, I2C,PWM
from time import sleep
import ssd1306


# 初始化I2C
i2c = I2C(1, scl=Pin(21), sda=Pin(22))


# 换向引脚
pin13 = Pin(13, Pin.OUT, value=1)

#油门14
pin14 = PWM(Pin(14))
pin14.freq(1000)

#刹车-低电平 16
pin16 = Pin(16, Pin.OUT, value=1)

# 初始化OLED显示屏
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# 初始化按钮
select_button = Pin(18, Pin.IN, Pin.PULL_DOWN)
confirm_button = Pin(19, Pin.IN, Pin.PULL_DOWN)

# 定义变量
current_gear = 1
direction = 0
rect_xy = [(0, 26), (73, 26), (0, 46), (73, 46), (0, 46), (68, 46)] # 矩形框四个位置
rect_index = 0 # 记录当前矩形框位置
gear_dict = {1:"1st", 2:"2nd", 3:"3rd"} # 档位显示字典
mod = 0 # 当前模式 main_frame

# 绘制主屏幕
def draw_main_frame():
    # 清屏
    oled.fill(0)

    # 标题
    oled.text('Func', 0, 10)
    oled.text(f'{gear_dict.get(current_gear)}', 80, 10)

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

    # 清屏
    oled.fill(0)

    oled.text('Mod1', 0, 10)
    oled.text(f'{gear_dict.get(current_gear)}', 80, 10)
    oled.hline(0, 20, 128, 1)

    oled.text('select to go', 0, 25)
    oled.text('confirm to stop', 0, 35)
    oled.rect(rect_xy[rect_index][0], rect_xy[rect_index][1], 55, 16, 1)
    oled.text('OK?', 10,50)
    oled.text('cancel', 70, 50)

    oled.show()

# 绘制模式二
def draw_mod2_frame():

    # 清屏
    oled.fill(0)

    oled.text('Mod2', 0, 10)
    oled.text(f'{gear_dict.get(current_gear)}', 80, 10)
    oled.hline(0, 20, 128, 1)

    oled.text('auto go', 0, 25)
    oled.text('confirm to stop', 0, 35)
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
            rect_index = (rect_index + 1) % 4 if rect_index < 4 else 0
            draw_main_frame()
        elif mod == 1:
            rect_index = 9 - rect_index
            draw_mod1_frame()
        elif mod == 2:
            rect_index = 9 - rect_index
            draw_mod2_frame()
        elif mod ==11:
            pin14.duty(0)
            pin16.value(0)
        elif mod == 22:
            pin14.duty(0)
            pin16.value(0)
        while pin.value() == 1:
            sleep(0.01)  # 等待按钮释放
            n+=1
            if n>100 and confirm_button.value():
                mod=0
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
                pin13.value(0)
                sleep(5)
                pin13.value(1)

                direction = 1 - direction
                draw_main_frame()

            elif rect_index == 2: # 选择模式一
                rect_index = 4
                mod=1
                draw_mod1_frame()

            elif rect_index == 3: # 选择模式二
                rect_index = 4
                mod=2
                draw_mod2_frame()
        elif mod == 1:
            if rect_index == 4:
                mod = 11
                oled.fill_rect(0, 46, 128, 18, 0)
                oled.show()
            elif rect_index == 5:
                mod=0
                rect_index = 0
                draw_main_frame()
        elif mod == 2:
            if rect_index == 4:
                oled.fill_rect(0, 46, 128, 18, 0)
                oled.show()
                mod = 22
            elif rect_index == 5:
                rect_index = 0
                mod=0
                draw_main_frame()
        elif mod ==11:
            pin14.duty(420+current_gear*200)
            pin16.value(1)
        elif mod == 22:
            pin14.duty(420+current_gear*200)
            pin16.value(1)
        while pin.value() == 1:
            sleep(0.01)  # 等待按钮释放
            if select_button.value():
                pin16.value(0)
            else:
                pin16.value(1)

# 绘制主菜单
draw_main_frame()

# 监听按键, mod 0是main_frame
while True:
    #print(mod)
    pin16.value(1)# 保持不刹车
    pin14.duty(0)# 保持无油门
    if select_button.value() == 1:
        on_select_button_pressed(select_button)

    elif confirm_button.value() == 1:
        on_confirm_button_pressed(confirm_button)

    # # 设置按键中断
    # select_button.irq(trigger=Pin.IRQ_RISING, handler=on_select_button_pressed)
    # confirm_button.irq(trigger=Pin.IRQ_RISING, handler=on_confirm_button_pressed)