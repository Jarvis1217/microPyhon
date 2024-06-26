# mpu6050.py
from micropython import const
import ustruct
import time
import math

# MPU6050 registers
MPU6050_ADDRESS = const(0x68)
PWR_MGMT_1 = const(0x6B)
SMPLRT_DIV = const(0x19)
CONFIG = const(0x1A)
GYRO_CONFIG = const(0x1B)
ACCEL_CONFIG = const(0x1C)
INT_ENABLE = const(0x38)
ACCEL_XOUT_H = const(0x3B)
ACCEL_YOUT_H = const(0x3D)
ACCEL_ZOUT_H = const(0x3F)
TEMP_OUT_H = const(0x41)
GYRO_XOUT_H = const(0x43)
GYRO_YOUT_H = const(0x45)
GYRO_ZOUT_H = const(0x47)

class MPU6050:
    def __init__(self, i2c, address=MPU6050_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.buf = bytearray(14)

        # Wake up the MPU-6050 since it starts in sleep mode
        self.i2c.writeto_mem(self.address, PWR_MGMT_1, b'\x00')
        time.sleep(0.1)
        self.i2c.writeto_mem(self.address, SMPLRT_DIV, b'\x07')
        self.i2c.writeto_mem(self.address, CONFIG, b'\x00')
        self.i2c.writeto_mem(self.address, GYRO_CONFIG, b'\x00')
        self.i2c.writeto_mem(self.address, ACCEL_CONFIG, b'\x00')
        self.i2c.writeto_mem(self.address, INT_ENABLE, b'\x01')
        time.sleep(0.1)

    def _read(self, reg):
        self.i2c.readfrom_mem_into(self.address, reg, self.buf)
        return self.buf

    def _read_word(self, reg):
        high = self.i2c.readfrom_mem(self.address, reg, 1)
        low = self.i2c.readfrom_mem(self.address, reg+1, 1)
        return ustruct.unpack('>h', high + low)[0]

    @property
    def accel(self):
        self._read(ACCEL_XOUT_H)
        accel_x = ustruct.unpack('>h', self.buf[0:2])[0]
        accel_y = ustruct.unpack('>h', self.buf[2:4])[0]
        accel_z = ustruct.unpack('>h', self.buf[4:6])[0]
        return accel_x, accel_y, accel_z

    @property
    def gyro(self):
        self._read(GYRO_XOUT_H)
        gyro_x = ustruct.unpack('>h', self.buf[8:10])[0]
        gyro_y = ustruct.unpack('>h', self.buf[10:12])[0]
        gyro_z = ustruct.unpack('>h', self.buf[12:14])[0]
        return gyro_x, gyro_y, gyro_z

    @property
    def temperature(self):
        temp = self._read_word(TEMP_OUT_H)
        return temp / 340.0 + 36.53
    
    def get_angle(self):
        accel_data = self.accel
        x = accel_data[0]
        y = accel_data[1]
        z = accel_data[2]
        roll = math.atan2(-x, math.sqrt(y * y + z * z)) * 57.2958
        pitch = math.atan2(y, z) * 57.2958
        return roll, pitch
    
'''
from machine import I2C, Pin
from mpu6050 import MPU6050

# 初始化I2C
i2c = I2C(1, scl=Pin(6), sda=Pin(7))

# 初始化MPU6050传感器
mpu = MPU6050(i2c)

while True:
    roll, pitch = MPU6050.get_angle()
    print("Roll: {:.2f}, Pitch: {:.2f}".format(roll, pitch))
'''
