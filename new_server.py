import socket

host = ""  # Address of the socket
port = 9999  # Port of the socket

"""Server class"""


class Server:

    def __init__(self):
        """Socket Creation"""
        try:
            self.s = socket.socket()
        except socket.error as msg:  # IN case connection timed out and socket craetion is failed.
            print("Socket Creation error: " + str(msg))

    def bind_socket(self):
        """Binding the socket and listening for connection"""
        try:
            print("Binding the port " + str(port))
            self.s.bind((host, port))
            self.s.listen(5)

        except socket.error as msg:
            print("socket binding error: " + str(msg) + "\n" + "Retrying ....")
            self.bind_socket()

    def socket_accept(self):
        """Connection establishment with client"""
        conn, address = self.s.accept()
        print("connection has been established " + "with IP " + address[0] + " and port " + str(address[1]))
        choice_msg = "With which operation you would like to proceed with\n1.Echo\n2.File Transfer"
        self.recv_data(conn, choice_msg)
        conn.close()

    def recv_data(self, conn, msg):
        """Receiving data for choices"""
        conn.send(msg.encode())
        msg_recv = conn.recv(1024)
        print("=========Value received from client: ", msg_recv.decode(), "==========")
        conn.send(msg_recv)
        self.select_choice(conn, msg_recv)

    def select_choice(self, conn, choice):
        """Choice selected """
        if choice.decode() == "1":
            echo_str = "======You have choosed ECHO service !!!====== \n======If you want to exit from ECHO service then please Enter (Quit/Exit)======"
            conn.send(echo_str.encode())
            self.server_echo(conn)
        if choice.decode() == "2":
            self.server_fts()

    def server_echo(self, conn):
        """Echo Server """
        while True:
            recv_data = conn.recv(1024)
            decoded_data = recv_data.decode()
            print("Input received from client: ", decoded_data)
            if decoded_data == "Quit" or decoded_data == "quit" or decoded_data == "Exit" or decoded_data == "exit":
                conn.send("Disconnecting from server ...\a".encode())
                break
            conn.sendall(recv_data)
        conn.close()

    def server_fts(self):
        pass  # function fot FTS code will come


def main():
    """Main Function"""
    server_obj = Server()
    server_obj.bind_socket()
    server_obj.socket_accept()


if __name__ == "__main__":
    main()

