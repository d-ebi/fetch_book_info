# -*- coding: utf-8 -*-

import logging, logging.handlers
import os

def get_module_logger(module_name):
    log_level_env = 'MINERVA_LOG_LEVEL'
    handler_env = 'MINERVA_LOG_FILE'
    log_level = logging.WARNING if not log_level_env in os.environ else getattr(logging, os.environ[log_level_env])
    handler = logging.StreamHandler() \
        if not handler_env in os.environ \
        else logging.handlers.TimedRotatingFileHandler(os.environ['MINERVA_LOG_FILE'], when='W0', interval=1, backupCount=10)
    logger = logging.getLogger(module_name)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    
    return logger

