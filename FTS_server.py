import os
import sys
import database
from new_server import Server


class FtsServer:

    def __init__(self):
        # Create connection
        self.db = database.DatabaseConn()
        # Create table if table does not exists
        self.db.create_table()

    def send_and_rec_msg(self, conn, msg):
        conn.send(msg.encode())
        recv_frm_client = conn.recv(1024)
        print("Value received from client: ", recv_frm_client.decode())
        return recv_frm_client

    def admin_settings(self, conn):
        # TODO: admin func (close server connection, view, delete, add)
        pass

    def user_authentication(self, conn):
        """User Authentication """
        # Receive username and password from Client
        recv_username = self.send_and_rec_msg(conn, "Enter username: ")
        recv_password = self.send_and_rec_msg(conn, "Enter password: ")
        if recv_username == 'admin' and recv_password == 'admin':
            conn.send("Admin Settings".encode())
            return "Admin"
        else:
            result = self.db.get_user_by_name_and_pass(recv_username.decode(), recv_password.decode())
            if result:
                conn.send("User Authenticated".encode())
                return True
            else:
                conn.send("Invalid Username or Password".encode())
                return False

    def server_settings(self, conn):
        """For settings choice"""
        choice_msg3 = "You have choosed Settings options\n1.View Logging\n2.Create New User\nPlease choose from above option: "
        recv_ch_msg = self.send_and_rec_msg(conn, choice_msg3)

        if recv_ch_msg.decode() == '1':
            # TO DO: Add logging functionality
            pass
        elif recv_ch_msg.decode() == '2':
            # Receive username and password from Client
            recv_username = self.send_and_rec_msg(conn, "Enter username: ")
            recv_password = self.send_and_rec_msg(conn, "Enter password: ")
            res = self.db.create_user(recv_username.decode(), recv_password.decode())
            if res is None:
                print("User created successfully")
                conn.send("User created successfully".encode())
            else:
                print(res)
                conn.send(res.encode())
        else:
            conn.send("Invalid choice!!Please enter valid choice..".encode())

    def client_get(self, conn):
        filename = conn.recv(1024).decode('utf-8')
        print(filename)
        print(os.path.isfile(filename))
        if os.path.isfile(filename):
            pathFilename = str('EXISTS ' + str(os.path.getsize(filename)))
            arr1 = bytes(pathFilename, 'utf-8')
            conn.send(arr1)
            userResponse1 = conn.recv(1024)
            userResponse = userResponse1.decode('utf-8')
            if userResponse[:2] == 'OK':
                with open(filename, 'rb') as f:
                    bytes_to_send = f.read()
                    conn.send(bytes_to_send)
        else:
            conn.send(bytes('ERR', 'utf-8'))
        # TO DO : Get functionality
        # conn.close()

    def fts_server(self, conn):
        result = self.user_authentication(conn)
        if result == 'Admin':
            self.admin_settings(conn)
        elif result:
            choice_msg2 = "========= You have choosed FTS service !!!=========\n1. get (To download the file from the server)\n2. put (If you want to upload the file into the server).\n3. Enter into the setting mode\n4. Quit\nPlease choose from above option: "
            recv_msg = Server.recv_data(self, conn, choice_msg2)
            if recv_msg.decode() == '1':
                # Get functionality
                self.client_get(conn)
            elif recv_msg.decode() == '2':
                pass
                # TODO : Put functionality
            elif recv_msg.decode() == '3':
                self.server_settings(conn)
            elif recv_msg.decode() == '4':
                conn.send("Exiting...".encode())
            else:
                conn.send("Wrong choice entered!!".encode())
        else:
            print("Invalid username or password!!")
