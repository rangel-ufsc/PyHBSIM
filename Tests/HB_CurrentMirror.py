import numpy as np
import matplotlib.pyplot as plt

import setup
from PyHBSim import PyHBSim, Netlist
from PyHBSim.Analyses import MultiToneHarmonicBalance

y = PyHBSim('Diode Testbench')

i1 = y.add_iac('I1', 'n1', 'gnd', ac=3e-3, freq=1e6, phase=+90)
i2 = y.add_idc('I2', 'n1', 'gnd', dc=20e-3)

r1 = y.add_resistor('R1', 'n1', 'gnd', 200)
r2 = y.add_resistor('R2', 'n1', 'nc', 200)

i3 = y.add_idc('I3', 'nb', 'gnd', dc=10e-3)
q1 = y.add_bjt('Q1', 'nb', 'nc', 'gnd')
q2 = y.add_bjt('Q2', 'nb', 'nb', 'gnd')

# i3 = y.add_idc('I3', 'nx', 'gnd', dc=0.77)
# g1 = y.add_gyrator('G1', 'nx', 'nb', 'gnd', 'gnd', 1)

q1.options['Is'] = 1e-15
q1.options['Bf'] = 100
q1.options['Vaf'] = 20

hb = MultiToneHarmonicBalance('HB1', 1e6, 5)

converged, freqs, Vf, time, Vt = hb.run(y)

hb.plot_v('nc')
plt.show()

# n = 1
# plt.figure()
# plt.subplot(211)
# plt.plot(Vt[n,:])
# plt.grid()
# plt.subplot(212)
# plt.stem(freqs, abs(Vf[n,:]), use_line_collection=True, markerfmt='^')
# for f, v in zip(freqs, Vf[n,:]):
#     label = "({:.3f}, {:.1f})".format(abs(v), np.degrees(np.angle(v)))
#     plt.annotate(label, (f,abs(v)), textcoords="offset points", xytext=(0,10), ha='center')
# plt.grid()
# plt.show()
