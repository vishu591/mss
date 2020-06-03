import sys
import socket

import FileTransferService
from msslogger import MSSLogger

MSSLogger.intializelogger()
logger = MSSLogger.getlogger("clientlogger")
host = "127.0.0.1"
port = 9999


class Client:
    def __init__(self):
        """Socket Creation"""
        try:
            logger.info("creating a socket connection")
            self.s = socket.socket()
            self.s.connect((host, port))
     
        except socket.error as msg:  # IN case connection timed out and socket creation is failed.
            print("Socket Creation error: " + str(msg))
            sys.exit(1)

    def select_choice(self):
        try:
            choice_msg = self.s.recv(1024)
            logger.info("======== Received choice message from server: =========\n "+ choice_msg.decode())
            print("======== Received choice message from server: =========\n ", choice_msg.decode())
            
            # User will provide the input as he wants to use the service
            choice_in = input("Please choose the functionality you want to proceed with: ")
            logger.info("Please choose the functionality you want to proceed with: "+ choice_in)
            
            self.s.send(choice_in.encode())

            choice_rec = self.s.recv(1024)       # According to selected choice, look for the service
            logger.info(choice_rec.decode())
            self.select_choice_part(choice_rec)

        except KeyboardInterrupt:
            print("Closing the socket as interrupted by user")
            sys.exit(1)

        except socket.error as msg:  # IN case connection timed out and socket creation is failed.
            print("Socket Creation error: " + str(msg))
            sys.exit(1)

    def select_choice_part(self, choice_rec):
        try:
            if choice_rec.decode():
                if choice_rec.decode() == '1':
                    echo_rcv = self.s.recv(1024).decode()
                    print(echo_rcv)

                    logger.info(echo_rcv)
                    self.client_echo()

                elif choice_rec.decode() == '2':
                    self.file_transfer()
                else:
                    print(self.s.recv(1024).decode())
                    logger.error(self.s.recv(1024).decode())
            else:
                print("Warning: Ack not received from server ")
        except socket.error as msg:  # IN case connection timed out and socket creation is failed.
            sys.exit(1)

    def client_echo(self):
        while True:
            msg = input("Enter the string: ")
            logger.info("Enter the string: "+msg)
            
            # send msg to server
            self.s.sendall(msg.encode())

            # echo reply from server
            data = self.s.recv(1024)
            print("Received echo message from server: ", data.decode())
            logger.info("Received echo message from server: "+data.decode())
            
            if data.decode() == "Disconnecting from server ...\a":
                break
        self.s.close()

    def file_transfer(self):
        fts_obj = FileTransferService.FileTransfer()
        fts_obj.fts_client(self.s)


def main():
    client_obj = Client()
    client_obj.select_choice()


if __name__ == "__main__":
    main()
