# import board
# import busio
# import digitalio
# import time
# import struct

# i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# i2c.try_lock()

# def reg_read_int16(dev_addr, reg_addr):
#     """Reads register `reg_addr` on device `dev_addr`"""
#     result = bytearray(2)
#     i2c.writeto_then_readfrom(
#         dev_addr,
#         bytes([reg_addr]),
#         result)
#     return struct.unpack(">h", result)[0]

# def reg_write(dev_addr, reg_addr, value):
#     """Write `value` to register `reg_addr` on device `dev_addr`"""
#     buf = bytearray([reg_addr, value // 256, value % 256])
#     i2c.writeto(dev_addr, buf)

# def led_set(dev_addr, value):
#     """Toggle LED by manipulating bus-undervoltage alert bit"""
#     if value:
#         reg_write(dev_addr, 0x06, 0x0000)
#     else:
#         reg_write(dev_addr, 0x06, 0x1000)

# def shunt_read(dev_addr):
#     """Shunt reading in amperes, positive charge, negative discharge"""
#     # LSB is 2.5uV
#     # Shunts are 75mV per 100A
#     return - reg_read_int16(dev_addr, 0x01) * 3.33e-3

# def bus_read(dev_addr):
#     """Bus reading in volts"""
#     # LSB is 1.25mV
#     return reg_read_int16(dev_addr, 0x02) * 1.25e-3

# led = False

# # Accumulated energy in watt-hours (starts counting from charged)
# alpha_accum = 1280
# beta_accum = 1280
# gamma_accum = 1280

# # set alert limit to max possible bus-voltage so toggling
# # the bus-voltage undervoltage alert bit toggles the LED
# try:
#     reg_write(0x40, 0x07, 0x7fff)
# except:
#     pass

# try:
#     reg_write(0x41, 0x07, 0x7fff)
# except:
#     pass

# try:
#     reg_write(0x42, 0x07, 0x7fff)
# except:
#     pass

# last_time = time.monotonic()

# # below is sloppy math for a sanity check - will refactor to properly average and integrate
# while True:
#     current_time = time.monotonic()
#     delta_time = current_time - last_time

#     try:
#         alpha_shunt = shunt_read(0x40)
#         alpha_bus = bus_read(0x40)
#     except:
#         alpha_shunt = None
#         alpha_bus = None
    
#     if alpha_shunt is not None and alpha_bus is not None:
#         alpha_accum += alpha_shunt * alpha_bus * delta_time / 3600.0
    
#     try:
#         beta_shunt = shunt_read(0x41)
#         beta_bus = bus_read(0x41)
#     except:
#         beta_shunt = None
#         beta_bus = None

#     if beta_shunt is not None and beta_bus is not None:
#         beta_accum += beta_shunt * beta_bus * delta_time / 3600.0

#     try:
#         gamma_shunt = shunt_read(0x42)
#         gamma_bus = bus_read(0x42)
#     except:
#         gamma_shunt = None
#         gamma_bus = None

#     if gamma_shunt is not None and gamma_bus is not None:
#         gamma_accum += gamma_shunt * gamma_bus * delta_time / 3600.0

#     last_time = current_time

#     led = not led

#     try:
#         led_set(0x40, led)
#     except:
#         pass
    
#     try:
#         led_set(0x41, led)
#     except:
#         pass
    
#     try:
#         led_set(0x42, led)
#     except:
#         pass

    
#     print("{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(
#         alpha_bus, alpha_shunt, alpha_accum,
#         beta_bus, beta_shunt, beta_accum,
#         gamma_bus, gamma_shunt, gamma_accum,
#         alpha_accum + beta_accum + gamma_accum))

#     time.sleep(0.1)

def main():
    from i2cbus import I2CBus
    from ina226 import INA226

    i2c = I2CBus()

    devices = [
        INA226(i2c, 0x40),
        INA226(i2c, 0x41),
        INA226(i2c, 0x42)
    ]

if __name__ == "__main__":
    main()
