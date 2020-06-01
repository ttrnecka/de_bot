import os
import logging
from logging.handlers import RotatingFileHandler

ROOT = os.path.dirname(__file__)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.propagate = False
handler = RotatingFileHandler(
    os.path.join(ROOT, '..', 'logs','discord.log'), maxBytes=1000000,
    backupCount=5, encoding='utf-8', mode='a'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)