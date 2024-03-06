import logging

# variables to control the logging levels
pyhbsim_level = logging.ERROR
dc_level = logging.ERROR
ac_level = logging.ERROR
tr_level = logging.ERROR
hb_level = logging.ERROR

formatter = logging.Formatter('[%(levelname)s]: %(name)s: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

""" PyHBSim Logger """
pyhbsim_logger = logging.getLogger('PyHBSim.PyHBSim')
pyhbsim_logger.setLevel(pyhbsim_level)

pyhbsim_logger.addHandler(stream_handler)

""" DC Analysis Logger """
dc_logger = logging.getLogger('PyHBSim.Analyses.DC')
dc_logger.setLevel(dc_level)

dc_logger.addHandler(stream_handler)

# file_handler = logging.FileHandler('DC.log')
# file_handler.setFormatter(formatter)
# dc_logger.addHandler(file_handler)

""" AC Analysis Logger """
ac_logger = logging.getLogger('PyHBSim.Analyses.AC')
ac_logger.setLevel(ac_level)

ac_logger.addHandler(stream_handler)

#file_handler = logging.FileHandler('AC.log')
#file_handler.setFormatter(formatter)
#ac_logger.addHandler(file_handler)

""" Transient Analysis Logger """
tr_logger = logging.getLogger('PyHBSim.Analyses.Transient')
tr_logger.setLevel(tr_level)

tr_logger.addHandler(stream_handler)

#file_handler = logging.FileHandler('TRAN.log')
#file_handler.setFormatter(formatter)
#tr_logger.addHandler(file_handler)

""" Harmonic Balance Analysis Logger """
hb_logger = logging.getLogger('PyHBSim.Analyses.HarmonicBalance')
hb_logger.setLevel(hb_level)

hb_logger.addHandler(stream_handler)

#file_handler = logging.FileHandler('HB.log')
#file_handler.setFormatter(formatter)
#hb_logger.addHandler(file_handler)
