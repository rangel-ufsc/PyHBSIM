import numpy as np
import matplotlib.pyplot as plt

import setup
from yalrf import YalRF, Netlist
from yalrf.Analyses import HarmonicBalance, HarmonicBalance2

y = YalRF('Diode Testbench')

i1 = y.add_iac('I1', 'n1', 'gnd', ac=20e-3, phase=+90)
i2 = y.add_idc('I2', 'n1', 'gnd', dc=5e-3)

r1 = y.add_resistor('R1', 'n1', 'gnd', 100)
r2 = y.add_resistor('R2', 'n2', 'gnd', 100)

d1 = y.add_diode('D1', 'n1', 'n2')

d1.options['Is'] = 1e-15
d1.options['N'] = 1
d1.options['Area'] = 1

hb = HarmonicBalance('HB1', 1e6, 10)

x = hb.run(y)
