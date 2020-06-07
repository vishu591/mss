from FileTransfer import FTS_server, FTS_client

from Logging.MSSlogger import MSSLogger

MSSLogger.intializelogger()
class FileTransfer(FTS_client.FtsClient, FTS_server.FtsServer):
    logger = MSSLogger.getlogger("serverlogger")
    pass

