import logging
class Serverhandler():
    def myLogging(self,fileName):
        logger = logging.getLogger("clientlogger")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(fileName+".log","w")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger=logger
        return logger
