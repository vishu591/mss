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
    threadCount = 0

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
            print("Waiting for incoming connection....")
        
        except KeyboardInterrupt:
            print("Closing the socket as interrupted by user")
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
                self.threadCount += 1
                self.logger.info('Thread Number:' + str(self.threadCount))
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
            choice_msg = "With which operation you would like to proceed with\n1.Echo\n2.File Transfer:"+str(self.threadCount)
            conn.send(choice_msg.encode())
            msg_recv = conn.recv(1024)
            list = str(msg_recv.decode()).split(":")
            self.logger.info("######## Client ",list[0]," Requested for '" + self.selected_service(list[1]) + "' Service ########")
            print("######## Client ",list[0]," Requested for '" + self.selected_service(list[1]) + "' Service ########")
            conn.send(list[1].encode())
            self.select_choice(conn, list[1].encode())
        except socket.error as msg:
            self.logger.info("Socket error: " + str(msg))
            sys.exit(1)

    def selected_service(self, select_service):
        try:
            if select_service == '1':
                selected_service = "Echo"
            elif select_service == '2':
                selected_service = "File Transfer"
            else:
                selected_service = "Invalid"
            return selected_service
        except socket.error as msg:
            self.logger.info("error while fetching service name: " + str(msg))

    def select_choice(self, conn, choice):
        """Choice selected """
        if choice.decode() == "1":
            echo_str = "========= You have choosed ECHO service !!!=========\n=========If you want to exit from ECHO service then please Enter (Quit/Exit) ========="
            conn.send(echo_str.encode())
            self.server_echo(conn)
        
        elif choice.decode() == "2":
            self.server_fts(conn)

        else:	
            conn.send("Wrong choice entered!!!\nExiting...".encode())

    def server_echo(self, conn):
        """Echo Server """
        while True:
            try:
                recv_data = conn.recv(1024)
                plain_text = recv_data.decode()
                self.logger.info("Input received from client: "+plain_text)
                print("Input received from client: ", plain_text)
                if plain_text.lower() == "quit" or plain_text.upper() == "QUIT" or plain_text.lower() == "exit" or plain_text.upper() == "EXIT":
                    conn.send("Disconnecting from server ...\a".encode())
                    break
                conn.sendall(recv_data)
            except socket.error as msg:
                print("socket connection failure", str(msg))
                sys.exit(1)
            if not len(recv_data):
                print("Closing the socket as interrupted by user in client side: No input received")
                break
        conn.close()

    def server_fts(self, conn):
        """ FTS GET functionality """
        fts_obj = FileTransferService.FileTransfer()	
        fts_obj.fts_server(conn)

def main():
    """Main Function"""
    server_obj = Server()
    server_obj.bind_socket()
    server_obj.socket_accept()


if __name__ == "__main__":
    main()

