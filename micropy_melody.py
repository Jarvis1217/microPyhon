from machine import Pin, PWM
from time import sleep

# 创建PWM对象
buzzer = PWM(Pin(10))

# 定义七音阶的频率 (C大调: C, D, E, F, G, A, B, C)
tones = {
    'C': 261,
    'D': 296,
    'E': 329,
    'F': 349,
    'G': 392,
    'A': 440,
    'B': 493
}

# 欢乐颂的完整音符和时值
melody = [
    ('E', 0.5), ('E', 0.5), ('F', 0.5), ('G', 0.5),
    ('G', 0.5), ('F', 0.5), ('E', 0.5), ('D', 0.5),
    ('C', 0.5), ('C', 0.5), ('D', 0.5), ('E', 0.5),
    ('E', 0.75), ('D', 0.25), ('D', 1.0),

    ('E', 0.5), ('E', 0.5), ('F', 0.5), ('G', 0.5),
    ('G', 0.5), ('F', 0.5), ('E', 0.5), ('D', 0.5),
    ('C', 0.5), ('C', 0.5), ('D', 0.5), ('E', 0.5),
    ('D', 0.75), ('C', 0.25), ('C', 1.0),

    ('D', 0.5), ('D', 0.5), ('E', 0.5), ('C', 0.5),
    ('D', 0.5), ('E', 0.2), ('F', 0.25), ('E', 0.5), ('C', 0.5),
    ('D', 0.5), ('E', 0.2), ('F', 0.25), ('E', 0.5), ('D', 0.5),
    ('C', 0.5), ('D', 0.5), ('G', 0.5),

    ('E', 0.5), ('E', 1), ('F', 0.5), ('G', 0.5),
    ('G', 0.5), ('F', 0.5), ('E', 0.5), ('D', 0.5),
    ('C', 0.5), ('C', 0.5), ('D', 0.5), ('E', 0.5),
    ('D', 0.75), ('C', 0.25), ('C', 1.0)
]

def play_tone(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty(340)  # 设置占空比
    sleep(duration)
    buzzer.duty(0)    # 停止蜂鸣器

# 播放欢乐颂
for note, duration in melody:
    if note in tones:
        play_tone(tones[note], duration)
    sleep(0.1)

# 关闭PWM
buzzer.deinit()