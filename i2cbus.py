import busio


class I2CBus:
    """Implement I2C read/write functionality"""

    def __init__(self):
        """Initialize I2C device"""
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
        self.i2c.try_lock()

    def reg_read_int16(self, dev_addr, reg_addr):
        """Reads register `reg_addr` on device `dev_addr`"""
        result = bytearray(2)
        self.i2c.writeto_then_readfrom(
            dev_addr,
            bytes([reg_addr]),
            result)
        return struct.unpack(">h", result)[0]

    def reg_write_int16(self, dev_addr, reg_addr, value):
        """Write `value` to register `reg_addr` on device `dev_addr`"""
        buf = bytearray([reg_addr, value // 256, value % 256])
        self.i2c.writeto(dev_addr, buf)
