import logging
import os

from config import ROOT_PATH

logger = logging.getLogger('nlp')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(ROOT_PATH, 'sys.log'))
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)