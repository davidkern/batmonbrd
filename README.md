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
