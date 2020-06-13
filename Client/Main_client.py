import os
import sys
import socket
import time

from cfonts import render

from FileTransfer import FileTransferService
from Logging.MSSlogger import MSSLogger


host = "127.0.0.1"
port = 9997


class Client:
    logger = ""
    clientThreadCount = 0
    max_pwd_try_count=3

    def __init__(self):
        """Socket Creation"""
        try:
            self.s = socket.socket()
            self.s.connect((host, port))

        except socket.error as msg:  # IN case connection timed out and socket creation is failed.
            print("Socket Creation error: " + str(msg))
            sys.exit(1)

    def select_choice(self):
        try:
            choice_msg = self.s.recv(1024)
            list = str(choice_msg.decode()).split(":")
            self.logger = MSSLogger.getClientLogger("Client" + list[1])
            self.clientThreadCount = list[1]

            width = os.get_terminal_size().columns

            output = render('Welcome To MSS', font='simple', colors=['red', 'yellow'], align='center', size=(150, width),
                             line_height=0)
            print(output, list[0])
            self.logger.info(output + list[0])

            # User will provide the input as he wants to use the service
            choice_in = input("Please choose the functionality you want to proceed with: ")
            self.logger.info("Please choose the functionality you want to proceed with: " + choice_in)
            self.s.send((list[1] + ":" + choice_in).encode())
            choice_rec = self.s.recv(1024)  # According to selected choice, look for the service
            self.logger.info(choice_rec.decode())
            time.sleep(2)
            os.system("cls")
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
                    # green color
                    print("\033[1;32;40m")  # green color
                    print("You have choosed ECHO service !!!" .center(os.get_terminal_size().columns))
                    print("\033[0;37;40m")  # normal text
                    print(echo_rcv.center(os.get_terminal_size().columns))
                    self.logger.info(echo_rcv)

                    self.client_echo()

                elif choice_rec.decode() == '2':
                    print("\033[1;32;40m")  # green color
                    print("You have choosed FTS service !!!".center(os.get_terminal_size().columns))
                    print("\033[0;37;40m")  # normal text
                    print("To proceed further, please enter your credentials".center(os.get_terminal_size().columns))
                    self.logger.info("To proceed further, please enter your credentials")
                    self.file_transfer()
                else:
                    print("\033[1;31;40m")  # red color
                    print(self.s.recv(1024).decode().center(os.get_terminal_size().columns))
                    print("\033[0;37;40m")  # normal text
                    # self.logger.error(self.s.recv(1024).decode())
                    sys.exit(1)

            else:
                print("\033[1;31;40m")  # red color
                print("Warning: Ack not received from server ")
                print("\033[0;37;40m")  # normal text

        except socket.error as msg:  # IN case connection timed out and socket creation is failed.
            print("Socket Creation error: " + str(msg))
            sys.exit(1)

    def client_echo(self):
        print("\n")
        while True:
            msg = input("Please provide the input: ")
            if len(msg) == 0:
                continue
            self.logger.info("Please provide the input: " + msg)

            # send msg to server
            self.s.sendall((str(self.clientThreadCount)+":"+msg).encode())

            # echo reply from server
            data = self.s.recv(1024)

            # if msg is for quit connection will close using break statement
            if data.decode() == "Disconnecting from server ...\a":
                print("\033[1;32;40m")  # green color
                print(data.decode())
                print("\033[0;37;40m")  # normal text
                break

            print("\033[1;32;40m")  # green color
            print("Received echo message from server: ", data.decode())
            print("\033[0;37;40m")  # normal text
            self.logger.info("Received echo message from server: " + data.decode())
        self.s.close()

    def file_transfer(self):
        """client code for fts get functionality"""
        fts_obj = FileTransferService.FileTransfer()
        fts_obj.fts_client(self.s, self.clientThreadCount, self.logger,self.max_pwd_try_count)
