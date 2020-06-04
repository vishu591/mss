import sys
import socket
import os
import threading
import FileTransferService
from _thread import *

from msslogger import MSSLogger

host = ""  # Address of the socket
port = 9999  # Port of the socket

MSSLogger.intializelogger()

class Server:
    """Server class"""
    logger = MSSLogger.getlogger("serverlogger")
    ThreadCount=0

    def __init__(self):
        """Socket Creation"""
        try:
            self.logger.info("creating a socket connection")
            self.s = socket.socket()
        except socket.error as msg:
            print("Socket Creation error: " + str(msg))
            sys.exit(1)

    def bind_socket(self):
        """Binding the socket and listening for connection"""
        try:
            print("Binding the port ..." + str(port))
            self.s.bind((host, port))
            print ("Waiting for incoming connection....")
        
        except KeyboardInterrupt:
            print ("Closing the socket as interupted by user")
            sys.exit(1)

        except socket.error as msg:
            self.logger.error("socket binding error: " + str(msg) + "\n" + "Retrying ....")
            print("socket binding error: " + str(msg) + "\n" + "Retrying ....")
            self.bind_socket()

    def socket_accept(self):
        try:
            """Connection establishment with client"""
            while True:
                self.s.listen(5)
                conn, address = self.s.accept()
                self.logger.info("connection has been established " + "with IP " + address[0] + " and port " + str(address[1]))
                print("connection has been established " + "with IP " + address[0] + " and port " + str(address[1]))
                self.ThreadCount += 1
                self.logger.info('Thread Number:'+ str(self.ThreadCount))
                start_new_thread(self.send_choice, (conn,))
        except KeyboardInterrupt:
            print("Closing the socket as interupted by user")
            sys.exit(1)

        except socket.error as msg:  # IN case connection timed out and socket creation is failed.
            print("Socket Creation error: " + str(msg))
            sys.exit(1)
        conn.close()

    def recv_data(self, conn, msg):
        """Receiving data for choices"""
        try:
            conn.send(msg.encode())
            msg_recv = conn.recv(1024)
            self.logger.info("========= Value received from client: " + msg_recv.decode() + "==========")
            print("========= Value received from client: ", msg_recv.decode(), "==========")
            conn.send(msg_recv)
            return msg_recv

        except socket.error as msg:
            self.logger.info("Socket error: " + str(msg))
            sys.exit(1)

    def send_choice(self, conn):
        """Receiving data for choices"""
        try:
            choice_msg = "With which operation you would like to proceed with\n1.Echo\n2.File Transfer"
            conn.send(choice_msg.encode())
            msg_recv = conn.recv(1024)
            self.logger.info("========= Value received from client: " + msg_recv.decode() + "==========")
            print("========= Value received from client: ", msg_recv.decode(), "==========")
            conn.send(msg_recv)
            self.select_choice(conn, msg_recv)
        except socket.error as msg:
            self.logger.info("Socket error: " + str(msg))
            sys.exit(1)

    def select_choice(self, conn, choice):
        """Choice selected """
        if choice.decode() == "1":
            echo_str = "========= You have choosed ECHO service !!!=========\n=========If you want to exit from ECHO service then please Enter (Quit/Exit) ========="
            conn.send(echo_str.encode())
            self.server_echo(conn)
        
        elif choice.decode() == "2":
            echo_str = "========= You have choosed FTS service !!!=========\nPlease choose from below option.\n1. get (To download the file from the server)\n2. put (If you want to upload the file into the server).\n3. Enter into the setting mode"
            conn.send(echo_str.encode())
            self.server_fts(conn)

        else:	
            conn.send("Wrong choice entered!!!\nExiting...".encode())

    def server_echo(self, conn):
        """Echo Server """
        while True:
            try:
                recv_data = conn.recv(1024)
                decoded_data = recv_data.decode()
                self.logger.info("Input received from client: "+decoded_data)
                print("Input received from client: ", decoded_data)
                if decoded_data == "Quit" or decoded_data == "quit" or decoded_data == "Exit" or decoded_data == "exit":
                    conn.send("Disconnecting from server ...\a".encode())
                    break
                conn.sendall(recv_data)
            except socket.error as msg:
                print("socket connection failure" , str(msg))
                sys.exit(1)
            if not len(recv_data):
                print ("Closing the socket as interupted by user in client side: No input received")
                break
        conn.close()

    def server_fts(self, conn):
        """ FTS GET functionality """
        fts_obj = FileTransferService.FileTransfer()	
        fts_obj.fts_server(conn)

        filename = conn.recv(1024).decode('utf-8')
        print (filename)
        print(os.path.isfile(filename))
        if os.path.isfile(filename):
            pathFilename = str('EXISTS ' + str(os.path.getsize(filename)))
            arr1 = bytes(pathFilename, 'utf-8')
            conn.send(arr1)
            userResponse1 = conn.recv(1024)
            userResponse = userResponse1.decode()
            if userResponse[:2] == 'OK':
                with open(filename, 'rb') as f:
                    bytes_to_send = f.read(1024)
                    conn.send(bytes_to_send)
        else:
            conn.send(bytes('ERR', 'utf-8'))
        conn.close()

def main():
    """Main Function"""
    server_obj = Server()
    server_obj.bind_socket()
    server_obj.socket_accept()


if __name__ == "__main__":
    main()

