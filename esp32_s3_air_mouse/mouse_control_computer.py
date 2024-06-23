import socket
import pyautogui
import threading


# 设置pyautogui的参数以减少操作延迟
pyautogui.MINIMUM_DURATION = 0  # 最小持续时间，0意味着立即移动
pyautogui.MINIMUM_SLEEP = 0     # 最小睡眠时间，减少延迟
pyautogui.PAUSE = 0.01          # 在执行动作之间增加的轻微延迟


def handle_command(command):
    if command == 'left':
        pyautogui.moveRel(-5, 0)
    elif command == 'right':
        pyautogui.moveRel(5, 0)
    elif command == 'up':
        pyautogui.moveRel(0, -5)
    elif command == 'down':
        pyautogui.moveRel(0, 5)
    elif command == 'stop':
        # 实现停止逻辑
        pass

def listen_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 12345))

    while True:
        data, addr = udp_socket.recvfrom(1024)
        command = data.decode()
        print(f"收到来自{addr}的指令：{command}")
        # 使用线程处理鼠标移动
        threading.Thread(target=handle_command, args=(command,)).start()

# 启动监听函数
listen_thread = threading.Thread(target=listen_udp)
listen_thread.start()