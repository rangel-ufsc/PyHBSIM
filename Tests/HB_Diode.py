import numpy as np
import matplotlib.pyplot as plt

import setup
from PyHBSim import PyHBSim, Netlist
from PyHBSim.Analyses import MultiToneHarmonicBalance

y = PyHBSim('Diode Testbench')

i1 = y.add_iac('I1', 'nx', 'gnd', ac=5, freq=1e6)
g1 = y.add_gyrator('G1', 'nx', 'n1', 'gnd', 'gnd', 1)

r1 = y.add_resistor('R1', 'n1', 'n2', 100)

d1 = y.add_diode('D1', 'gnd', 'n2')

d1.options['Is'] = 1e-15
d1.options['N'] = 1
d1.options['Area'] = 1

hb = MultiToneHarmonicBalance('HB1', 1e6, 10)

converged, freqs, Vf, time, Vt = hb.run(y)

hb.plot_v('n1')
hb.plot_v('n2')
plt.show()
