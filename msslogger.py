import logging
import logging.config

# MSS logger file
class MSSLogger:

    # this method initialize the logger
    @staticmethod
    def intializelogger():
        logging.config.fileConfig(fname='log.ini', disable_existing_loggers=False)

    # this method returns the logger instance based on the logger name from log.ini config file
    @staticmethod
    def getlogger(loggerName):
        logger = logging.getLogger(loggerName)
        return logger
