import unittest
import main
import collections
import ina226


class FakeINA226:
    """Implements a faked INA226 for testing"""
    REG_CONFIGURATION = 0
    REG_SHUNT_VOLTAGE = 1
    REG_BUS_VOLTAGE = 2
    REG_POWER = 3
    REG_CURRENT = 4
    REG_CALIBRATION = 5
    REG_MASK_ENABLE = 6
    REG_ALERT_LIMIT = 7
    REG_MANUFACTURER_ID = 8
    REG_DIE_ID = 9

    def __init__(self):
        """Initial conditions from datasheet"""
        self.registers = [
            0x4127,  # Configuration
            0x0000,  # Shunt Voltage
            0x0000,  # Bus Voltage
            0x0000,  # Power
            0x0000,  # Current
            0x0000,  # Calibration
            0x0000,  # Mask/Enable
            0x0000,  # Alert Limit
            0x5449,  # Manufacturer ID
            0x2260   # Die ID
        ]
    
    def read_int16(self, address):
        return self.registers[address]
    
    def write_int16(self, address, value):
        self.registers[address] = value


class FakeI2CBus:
    """Implements a faked I2C bus for testing"""
    def __init__(self):
        self.devices = {}
    
    def attach_device(self, address, device):
        """Attaches a faked device to the faked bus"""
        self.devices[address] = device
    
    def reg_read_int16(self, dev_addr, reg_addr):
        """Reads register `reg_addr` on device `dev_addr`"""
        return self.devices[dev_addr].read_int16(reg_addr)
        
    def reg_write_int16(self, dev_addr, reg_addr, value):
        """Write `value` to register `reg_addr` on device `dev_addr`"""
        return self.devices[dev_addr].write_int16(reg_addr, value)


class TestINA226(unittest.TestCase):
    def setUp(self):
        self.i2c = FakeI2CBus()
        self.i2c.attach_device(0x40, FakeINA226())
        self.dut = ina226.INA226Client(self.i2c, 0x40)
    
    def test_initial_conditions(self):
        """Test that state of charge is initially fully charged"""
        self.assertEqual(1280, self.dut.soc)

    def test_first_measurement_skips_integration(self):
        """Tests that first measurement does not integrate"""
        # set expectations
        # -1.23A shunt current and 12.8V bus voltage
        self.i2c.reg_write_int16(0x40, FakeINA226.REG_SHUNT_VOLTAGE, 369)
        self.i2c.reg_write_int16(0x40, FakeINA226.REG_BUS_VOLTAGE, 10240)

        measurement = self.dut.measurement(1000)

        self.assertEqual(1000, measurement.timestamp)
        self.assertTrue(abs(-1.23 - measurement.current) <= 0.01)
        self.assertEqual(12.8, measurement.voltage)
        self.assertEqual(1280, measurement.soc)

    
if __name__ == "__main__":
    unittest.main()
