# -*- coding: utf-8 -*-

import logging
import os

def get_module_logger(module_name):
    log_level_env = 'MINERVA_LOG_LEVEL'
    handler_env = 'MINERVA_LOG_FILE'
    log_level = logging.DEBUG if not log_level_env in os.environ else getattr(logging, os.environ[log_level_env])
    
    # TODO: filehandlerの場合、ログローテーションを入れる
    # TODO: ファイルも設定
    
    logger = logging.getLogger(module_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    
    return logger

