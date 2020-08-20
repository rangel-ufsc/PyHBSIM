import numpy as np

import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg

from yarf.Devices import *
from yarf.Analyses import DC

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(levelname)s]: %(name)s: %(message)s')

# file_handler = logging.FileHandler('AC.log')
# file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# logger.addHandler(file_handler) # enable file logging
logger.addHandler(stream_handler) # enable console logging

options = dict()
options['is_sparse'] = False
options['max_iterations'] = 150
options['gmin'] = 1e-12

# convergence parametes
options['reltol'] = 1e-3
options['vabstol'] = 1e-6
options['iabstol'] = 1e-12

class AC():
    
    def __init__(self, name, start, stop, numpts=10, stepsize=None, sweeptype='linear'):
        self.name = name

        self.xac = None # list of complex solutions
        self.xdc = None

        self.start = start
        self.stop = stop
        self.numpts = numpts
        self.stepsize = stepsize
        self.sweeptype = sweeptype
        
        self.n = 0     # number of uniquely named nodes including 'gnd'
        self.m = 0     # number of independent voltage sources
        self.devs = [] # list of devices
        self.iidx = {} # maps a indep. vsource idx in the MNA to a device
        
        self.options = options.copy() # AC simulation options

        if sweeptype == 'linear':
            if stepsize is not None:
                self.freqs = np.arange(start, stop, step)
            else:
                self.freqs = np.linspace(start, stop, numpts)
        elif sweeptype == 'logarithm':
            self.freqs = np.geomspace(start, stop, numpts)
        else:
            logger.warning('Failed to calculate the frequencies vector!')
            self.freqs = np.array([start, stop])

    def get_dc_solution(self):
        return self.xdc

    def get_ac_solution(self):
        return self.xac

    def get_freqs(self):
        return self.freqs

    def run(self, y, x0=None):
        # get netlist parameters and data structures
        self.n = y.get_n()
        self.m = y.get_m('ac')
        self.devs = y.get_devices()
        self.iidx = y.get_mna_extra_rows_dict('ac')

        # perform DC simulation if no operating point is provided
        if x0 is None:
            dc = DC(self.name + 'DC')
            self.xdc = dc.run(y)
        else:
            self.xdc = x0

        # calculate the operating point of nonlinear devices
        for dev in self.devs:
            if dev.is_nonlinear():
                dev.calc_oppoint(self.xdc)

        # Here we go!
        logger.info('Starting AC analysis.')

        # create MNA matrices
        A = np.zeros((self.n+self.m, self.n+self.m), dtype=complex)
        z = np.zeros((self.n+self.m, 1), dtype=complex)

        # create complex matrix to hold the AC solution
        self.xac = np.empty((len(self.freqs), len(z)-1), dtype=complex)

        k = 0
        for freq in self.freqs:
            # refresh the MNA matrices
            A[:][:] = 0
            z[:] = 0

            # populate the matrices A and z with the devices stamps
            for dev in self.devs:
                idx = self.iidx[dev] if dev in self.iidx else None
                dev.add_ac_stamps(A, z, self.xdc, idx, freq)

            # adding gmin to all nodes
            A = A + np.eye(len(A)) * self.options['gmin']

            # solve complex linear system
            xac, issolved = self.solve_ac_linear(A, z)

            # linear system is solved: add the solution to output
            # otherwise: add zeroes as solution and issue error log
            if issolved:
                self.xac[k] = np.transpose(xac)
            else:
                self.xac[k] = np.zeros((1, len(z)-1))
                logger.error('Failed to solve AC for frequency {}!', freq)

            logger.debug('A:\n{}\nz:\n{}\nxac\n{}'.format(A[1:,1:], z[1:], xac))
            k = k + 1

        logger.info('Finished AC analysis.')
        return self.xac

    def solve_ac_linear(self, A, z):
        if self.options['is_sparse'] == True:
            An = scipy.sparse.csc_matrix(A[1:,1:])
            lu = scipy.sparse.linalg.splu(An)
            xac = lu.solve(z[1:])
        else:
            lu, piv = scipy.linalg.lu_factor(A[1:,1:])
            xac = scipy.linalg.lu_solve((lu, piv), z[1:])

        return xac, not np.isnan(np.sum(xac))



