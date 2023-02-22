import logging                  # Manage logs and logging
from modules import environment              # Get DEBUG mode from environment

DEBUG = environment.DEBUG

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

fileHandler = logging.FileHandler('jarvis.log')
fileHandler.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)

# If .env file sets DEBUG to TRUE, it will output logs to python terminal in real time
if DEBUG == "TRUE":
    logger.addHandler(consoleHandler)

formatter = logging.Formatter('%(asctime)s: %(message)s', "%Y-%m-%d %H:%M:%S")
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
