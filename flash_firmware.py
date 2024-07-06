import serial.tools.list_ports
import subprocess
import time

def get_connected_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def execute_commands(port):
    commands = [
        f'esptool --chip esp32c3 --port {port} erase_flash',
        f'esptool --chip esp32c3 --port {port} --baud 460800 write_flash -z 0x0 C:\\Users\\lenovo\\Desktop\\c3_mini.bin',
        f'ampy --port {port} put mpu6050.py',
        f'ampy --port {port} put main.py'
    ]
    
    for command in commands:
        print(f"Executing: {command}")
        process = subprocess.Popen(command, shell=True)
        process.wait()  # 等待命令执行完毕
        time.sleep(1)   # 添加一个短暂的延迟，确保命令完全执行完毕

def main():
    previous_ports = set(get_connected_ports())
    
    while True:
        current_ports = set(get_connected_ports())
        new_ports = current_ports - previous_ports
        
        for port in new_ports:
            if port != 'COM3':
                execute_commands(port)
            print("DONE")
        
        previous_ports = current_ports
        time.sleep(1)

if __name__ == '__main__':
    main()
