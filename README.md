# batmonbrd - Battery Monitor Board

This code file is for a Serpente (https://www.tindie.com/products/arturo182/serpente-a-tiny-circuitpython-prototyping-board/) CircuitPython board
which monitors INA226 (https://www.ti.com/product/INA226) for the LiFePO4 batteries
in the Hab.

Bus and shunt voltages are read continuously for each of the three batteries.
An accumulated bus * shunt value is kept for each battery, which when multiplied
by a constant gives the total energy stored.

The alert pin of the INA226 is used as a GPIO to flash an LED.  This will be
used to indicate state of charge of the battery.

This was hacked together to be "good enough".  Future work will clean this up to
be consistent with other Hab devices.

# License

Either MIT or Apache license, at your option.

# Requirements

1. The INA226 chips are read over an I2C bus with a 100kHz clock (de-rated from 400kHz)
   to account for the additional bus capacitance due to the longer leads.
2. Chips are used in their boot configuration, which are continuous reads at approximately
   1ms each with no on-chip scaling.
3. An LED on each sensor is connected to the ALERT pin. The LED can be enabled by setting
   bit 13, Bus Voltage Over-Voltage, in the Mask/Enable register.
4. State-of-charge (SOC) for each battery is stored in Watt-hours, at device reset SOC is
   set to fully-charged, which is 1280 Whr.
5. The LED is flashed at 1-10Hz, in proportion to the corresponding battery's charge. At
   full charge, the LED flashes at 10Hz. At 10% state of charge or lower, the LED flashes
   at 1Hz.
6. Once per second a JSON-encoded list of battery state is sent to the host. The battery
   state is encoded as:
```
{
    "voltage": 13.50
    "current": 1.23
    "soc": 1280.00
}
```
7. Values are reported to the nearest 1/100th.
8. The host may send a JSON-encoded list, one element per battery, to set the state of
   charge.
9. If the battery voltage reaches 14.15 volts, then SOC is reset to fully charged and
   remains fully charged until battery voltage drops below 13.45 volts.
