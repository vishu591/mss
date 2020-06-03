import sys
import database
from new_server import Server


class FtsServer:

    def __init__(self):
        # Create connection
        self.db = database.DatabaseConn()
        # Create table if table does not exists
        self.db.create_table()

    def user_authentication(self, conn):
        """User Authentication """
        # Receive username and password from Client
        recv_username = Server.recv_data(self, conn, "Enter username:")
        recv_password = Server.recv_data(self, conn, "Enter password:")

        result = self.db.get_user_by_name_and_pass(recv_username.decode(), recv_password.decode())
        if result:
            conn.send("User Authenticated".encode())
            return True
        else:
            conn.send("User Credentials not exits".encode())
            return False

    def server_settings(self, conn):
        """For settings choice"""
        choice_msg3 = "For Settings, Select the correct option: 1.View Logging\n 2.Create New User"
        recv_ch_msg = Server.recv_data(self, conn, choice_msg3)
        if recv_ch_msg.decode() == '1':
            # TO DO: Add logging functionality
            pass
        elif recv_ch_msg.decode() == '2':
            recv_username = Server.recv_data(self, conn, "Enter username:")
            recv_password = Server.recv_data(self, conn, "Enter password:")
            self.db.create_user(recv_username.decode(), recv_password.decode())
            conn.send("User created successfully".encode())
        else:
            conn.send("Invalid choice!!Please enter valid choice..")

    def fts_server(self, conn):
        result = self.user_authentication(conn)
        if result:
            choice_msg2 = "For FTP, Select the correct option: 1.Get\n 2.Put\n3.Settings"
            recv_msg = Server.recv_data(self, conn, choice_msg2)
            if recv_msg.decode() == '1':
                pass
                # TO DO : Get functionality
            elif recv_msg.decode() == '2':
                pass
                # TO DO : Put functionality
            elif recv_msg.decode() == '3':
                self.server_settings(conn)
            else:
                conn.send("Wrong choice entered!!".encode())
                sys.exit(1)
        else:
            sys.exit(1)
