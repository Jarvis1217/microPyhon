import ustruct
import time


class Sensor:
    def __init__(self, i2c, address=0x29):
        self.i2c = i2c
        self._address = address
        self.init()
        self.default_settings()

    def _set_reg8(self, address, value):
        data = ustruct.pack('>HB', address, value)
        self.i2c.writeto(self._address, data)

    def _set_reg16(self, address, value):
        data = ustruct.pack('>HH', address, value)
        self.i2c.writeto(self._address, data)

    def _get_reg8(self, address):
        self.i2c.start()
        self.i2c.write(ustruct.pack('>BH', self._address << 1, address))
        data = self.i2c.readfrom(self._address, 1)
        return data[0]

    def _get_reg16(self, address):
        self.i2c.start()
        self.i2c.write(ustruct.pack('>BH', self._address << 1, address))
        data = self.i2c.readfrom(self._address, 2)
        return ustruct.unpack('>B', data)[0]

    def init(self):
        if self._get_reg8(0x0016) != 1:
            raise RuntimeError("Failure reset")

        # Recommended setup from the datasheet
        self._set_reg8(0x0207, 0x01) 
        self._set_reg8(0x0208, 0x01)
        self._set_reg8(0x0096, 0x00)
        self._set_reg8(0x0097, 0xfd)
        self._set_reg8(0x00e3, 0x00)
        self._set_reg8(0x00e4, 0x04)
        self._set_reg8(0x00e5, 0x02)
        self._set_reg8(0x00e6, 0x01)
        self._set_reg8(0x00e7, 0x03)
        self._set_reg8(0x00f5, 0x02)
        self._set_reg8(0x00d9, 0x05)
        self._set_reg8(0x00db, 0xce)
        self._set_reg8(0x00dc, 0x03)
        self._set_reg8(0x00dd, 0xf8)
        self._set_reg8(0x009f, 0x00)
        self._set_reg8(0x00a3, 0x3c)
        self._set_reg8(0x00b7, 0x00)
        self._set_reg8(0x00bb, 0x3c)
        self._set_reg8(0x00b2, 0x09)
        self._set_reg8(0x00ca, 0x09)
        self._set_reg8(0x0198, 0x01)
        self._set_reg8(0x01b0, 0x17)
        self._set_reg8(0x01ad, 0x00)
        self._set_reg8(0x00ff, 0x05)
        self._set_reg8(0x0100, 0x05)
        self._set_reg8(0x0199, 0x05)
        self._set_reg8(0x01a6, 0x1b)
        self._set_reg8(0x01ac, 0x3e)
        self._set_reg8(0x01a7, 0x1f)
        self._set_reg8(0x0030, 0x00)

    def default_settings(self):
        self._set_reg8(0x0011,0x10)
        self._set_reg8(0x010a, 0x30)
        self._set_reg8(0x003f, 0x46)
        self._set_reg8(0x0031, 0xFF)
        self._set_reg8(0x0041, 0x63)
        self._set_reg8(0x002e, 0x01)
        self._set_reg8(0x001b, 0x09)
        self._set_reg8(0x003e, 0x31)
        self._set_reg8(0x0014, 0x24)

    def identify(self):
        """Retrieve identification information of the sensor."""
        return {
            'model': self._get_reg8(0x0000),
            'revision': (self._get_reg8(0x0001), self._get_reg8(0x0002)),
            'module_revision': (self._get_reg8(0x0003),
                                self._get_reg8(0x0004)),
            'date': self._get_reg16(0x006),
            'time': self._get_reg16(0x008),
        }

    def address(self, address=None):
        """Change the I2C address of the sensor."""
        if address is None:
            return self._address
        if not 8 <= address <= 127:
            raise ValueError("Wrong address")
        self._set_reg8(0x0212, address)
        self._address = address

    def UpscaleSetScaling(self, new_scaling):
        DefaultCrosstalkValidHeight = 20
        ScalerValues = [0, 253, 127, 84]

        if new_scaling < 1 or new_scaling > 3:
            return

        scaling = new_scaling

        ptp_offset = self._get_reg8(0x0016)

        self._set_reg16(0x0096, ScalerValues[scaling])
        self._set_reg8(0x0024, ptp_offset // scaling)
        self._set_reg8(0x0021, DefaultCrosstalkValidHeight // scaling)
        self._get_reg8(0x002D)
        self._set_reg8(0x0021, DefaultCrosstalkValidHeight // scaling)

    def range(self):
        self._set_reg8(0x0018, 0x01) # Sysrange start
        time.sleep(0.01)
        return self._get_reg8(0x0062) # Result range value
    
"""
from machine import I2C, Pin
import vl6180x

i2c = I2C(scl=Pin(35), sda=Pin(36))

s = vl6180x.Sensor(i2c)

s.UpscaleSetScaling(3)

while True:
    dis = s.range() * 3
    print(f"{dis}mm")
"""