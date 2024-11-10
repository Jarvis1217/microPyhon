from machine import Pin, ADC
import time

# 定义摇杆引脚
x_pin = ADC(Pin(34))
y_pin = ADC(Pin(35))
button_pin = Pin(32, Pin.IN, Pin.PULL_DOWN)

# 设置ADC分辨率
x_pin.width(ADC.WIDTH_10BIT)
y_pin.width(ADC.WIDTH_10BIT)

# 设置ADC衰减
x_pin.atten(ADC.ATTN_11DB)
y_pin.atten(ADC.ATTN_11DB)

# EMA 滤波参数
EMA_ALPHA = 0.2  # EMA平滑因子，数值越小，滤波越强
DEAD_ZONE = 20   # 死区范围

# 初始化EMA值
ema_x = 512
ema_y = 512

while True:
    # 读取摇杆值
    raw_x = x_pin.read()
    raw_y = y_pin.read()
    
    # 计算EMA
    ema_x = EMA_ALPHA * raw_x + (1 - EMA_ALPHA) * ema_x
    ema_y = EMA_ALPHA * raw_y + (1 - EMA_ALPHA) * ema_y
    
    # 应用死区范围，并在接近中值时迅速回正
    if abs(ema_x - 512) < DEAD_ZONE:
        ema_x = 512
    if abs(ema_y - 512) < DEAD_ZONE:
        ema_y = 512
    
    # 读取按钮状态
    button_val = button_pin.value()
    
    # 打印结果
    print("X:", int(ema_x), "Y:", int(ema_y), "Button:", "Pressed" if button_val == 1 else "Released")
    
    # 延迟
    time.sleep(0.1)
