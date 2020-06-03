
import FTS_client
import FTS_server

from msslogger import MSSLogger

MSSLogger.intializelogger()


class FileTransfer(FTS_client.FtsClient,  FTS_server.FtsServer):
    logger = MSSLogger.getlogger("filetransfer")
    pass

