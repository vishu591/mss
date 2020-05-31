import logging
import random
import os
class serverFileHandler(logging.FileHandler):
    def __init__(self,fileName,mode):
        super(serverFileHandler,self).__init__(fileName,mode)