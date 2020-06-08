import logging
import logging.config
import glob

# MSS logger file
import os
from os import path
from pathlib import Path


class MSSLogger:

    # this method initialize the logger
    @staticmethod
    def intializelogger():
        final_directory = str(Path(os.getcwd()).parent) + "\Logs"
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        log_file_path = str(Path(os.getcwd()).parent)+ '\\log.ini'
        try:
            logging.config.fileConfig(fname=log_file_path, disable_existing_loggers=False)
        except:
            print("Exception occured while loading logging file...")


    # this method returns the logger instance based on the logger name from log.ini config file
    @staticmethod
    def getlogger(loggerName):
        logger = logging.getLogger(loggerName)
        return logger

    @staticmethod
    def getClientLogger(fileName):
        clientlogger = logging.getLogger("clientlogger")
        clientlogger.setLevel(logging.INFO)
        handler = logging.FileHandler(str(Path(os.getcwd()).parent)+"\Logs\\"+fileName+".log",'w')
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        clientlogger.addHandler(handler)
        return clientlogger
