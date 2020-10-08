import time


SOC_MAX = 1280  # Fully charged is 1280 Whr
LED_FREQUENCY_MAX = 10  # Frequency in Hz

class Measurement:
    """A moment-in-time measurement from the INA226"""

    def __init__(self, timestamp=0, voltage=0, current=0, soc=SOC_MAX):
        """
        Creates a measurement record.
        """
        self.timestamp = timestamp
        self.voltage = voltage
        self.current = current
        self.soc = soc
    
    def to_json(self):
        """
        Convert to json using string interpolation to work-around lack
        of (u)json module on serpente's CircuitPython
        """
        return f'{{"ts": {self.timestamp:f}, "voltage": {self.voltage:.3f}, "current": {self.current:.3f}, "soc": {self.soc:.3f}}}'


class INA226Client:
    """INA226 device on the I2C bus"""

    def __init__(self, i2c, address):
        """
        Initializes INA226 device object.

        Args:
            i2c: The i2c bus object
            address: The address of the INA226 on the bus
        """
        self.i2c = i2c
        self.address = address
        self.led_frequency = 0
        self.last_measurement = Measurement()
    
    def read_shunt(self):
        """Shunt reading in amperes, positive charge, negative discharge"""
        # LSB is 2.5uV
        # Shunts are 75mV per 100A
        return - self.i2c.reg_read_int16(self.address, 1) * 3.33e-3

    def read_bus(self):
        """Bus reading in volts"""
        # LSB is 1.25mV
        return self.i2c.reg_read_int16(self.address, 2) * 1.25e-3

    def measurement(self, timestamp=None):
        """Take a measurement"""
        if timestamp is None:
            timestamp = time.monotonic()

        measurement = Measurement(
            timestamp,
            self.read_bus(),
            self.read_shunt())
        
        # calculate new state of charge
        if self.last_measurement.timestamp != 0:
            delta = timestamp - self.last_measurement.timestamp
            if delta >= 0:
                # integrate using mean of the interval endpoints
                mean_voltage = (self.last_measurement.voltage + measurement.voltage) / 2.0
                mean_current = (self.last_measurement.current + measurement.current) / 2.0
                mean_power = mean_voltage * mean_current
                measurement.soc = self.last_measurement.soc + mean_power * delta / 3600.0
            else:
                # wrapped around, use last soc calculation
                measurement.soc = self.last_measurement.soc
        
        self.last_measurement = measurement

        return measurement

    @property
    def soc(self):
        return self.last_measurement.soc

    @property
    def voltage(self):
        return self.last_measurement.voltage
    
    @property
    def current(self):
        return self.last_measurement.current
