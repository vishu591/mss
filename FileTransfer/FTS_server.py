import os
import socket
import sys

from DAO import database
from Logging.MSSlogger import MSSLogger
from Server.Main_server import Server


class FtsServer:
    logger = MSSLogger.getlogger("serverlogger")
    max_pwd_try_count = 3

    def __init__(self):
        # Create connection
        self.db = database.DatabaseConn()
        # Create table if table does not exists
        self.db.create_table()

    def send_and_rec_msg(self, conn, msg):
        conn.send(msg.encode())
        recv_frm_client = conn.recv(1024)
        credentials = str(recv_frm_client.decode()).split(":")
        print("Value received from client", recv_frm_client.decode())
        return credentials[1].encode()

    def admin_settings(self, conn):
        """admin func (close connection, view, delete, add"""
        msg = "1. Close connection\n2. View all Users\n3. Add User\n4. Remove User\nChoose from above option: "
        conn.send(msg.encode())
        inp_rec = conn.recv(1024).decode()
        if inp_rec == '1':
            conn.send("Closing the connection by Admin".encode())
        elif inp_rec == '2':
            test_list = self.db.fetch_users_all()
            temp = list(map(' '.join, test_list))
            conn.send(str(temp).encode())
        elif inp_rec == '3':
            recv_username = self.send_and_rec_msg(conn, "Enter username: ")
            recv_password = self.send_and_rec_msg(conn, "Enter password: ")
            res = self.db.get_user_by_name(recv_username.decode())
            if len(res) == 0:
                print(self.db.create_user(recv_username.decode(), recv_password.decode()))
                conn.send("User created successfully".encode())
            else:
                conn.send("User already exists".encode())
        elif inp_rec == '4':
            recv_username = self.send_and_rec_msg(conn, "Enter username: ")
            res = self.db.get_user_by_name(recv_username.decode())
            if len(res) == 0:
                conn.send("User does not exists".encode())
            else:
                self.db.remove_user(recv_username.decode())
                conn.send("User Deleted successfully".encode())
        else:
            conn.send("Invalid choice!!".encode())

    def user_authentication(self, conn, pass_try_count):
        """User Authentication """
        # Receive username and password from Client
        if pass_try_count== 0:
            return False
        else:
            recv_username = self.send_and_rec_msg(conn, "Enter username: ")
            recv_password = self.send_and_rec_msg(conn, "Enter password: ")
            if recv_username.decode() == 'admin' and recv_password.decode() == 'admin':
                conn.send("Admin Settings".encode())
                return "Admin"
            else:
                result = self.db.get_user_by_name_and_pass(recv_username.decode(), recv_password.decode())
                if result:
                    conn.send("User Authenticated".encode())
                    return True
                else:
                    while pass_try_count > 0:
                        if pass_try_count >1:
                            conn.send("Invalid Username or Password.Please Try Again".encode())
                        return self.user_authentication(conn, pass_try_count - 1)


    def server_settings(self, conn):
        """For settings choice"""
        choice_msg3 = "You have choosed Settings options\n1.View Logging\n2.Create New User\nPlease choose from above option: "
        recv_ch_msg = self.send_and_rec_msg(conn, choice_msg3)

        if recv_ch_msg.decode() == '1':
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
        """this function is used for downloading the file from server to client"""
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

    def uploadFile(self, sock):
        """this function is user for uploading the file from client to server"""
        filename = sock.recv(1024)  # filename
        encodedFile = filename.decode()
        if os.path.isfile(encodedFile) and filename != "q":
            encodedFilename = sock.recv(1024).decode()  # concatinate size
            filesize = int(encodedFilename.split(" EXISTS ", 1)[1])
            finalfileName = encodedFilename.split(" EXISTS ", 1)[0]
            print("file which is going to be uploaded is : " + finalfileName)
            upload_filepath = sock.recv(1024)
            if upload_filepath.decode() == "":
                sock.send("No file path given".encode())
                print("No file path given")
            else:
                encodedFilePath = upload_filepath.decode()
                print(os.path.exists(encodedFilePath))
                if os.path.exists(encodedFilePath):
                    os.chdir(encodedFilePath)
                    print(finalfileName, " file will be available on path:", encodedFilePath)
                    filename1 = finalfileName[str(finalfileName).rfind("/"):]
                    f = open(encodedFilePath + "/" + filename1, 'wb')
                    data = sock.recv(1024)
                    total_recv = len(data)
                    f.write(data)
                    while total_recv < filesize:
                        data = sock.recv(1024)
                        total_recv += len(data)
                        f.write(data)
                    print("Upload complete")
                    sock.send("Upload complete".encode())
                else:
                    no_path = (f"file path '{encodedFilePath}' doesn't exist, Please try again")
                    print(no_path)
                    sock.send(no_path.encode())

        else:
            no_path = ("No filename given or user wants to quit")
            print(no_path)
            sock.send(no_path.encode())

    def fts_server(self, conn):
        self.db.create_user('admin', 'admin')
        result = self.user_authentication(conn, self.max_pwd_try_count)
        if result == 'Admin':
            self.admin_settings(conn)
        elif result:
            choice_msg2 = "1. get (To download the file from the server)\n2. put (If you want to upload the file into the server).\n3. Enter into the setting mode\n4. Quit\nPlease choose from above option: "
            recv_msg = Server.recv_data(self, conn, choice_msg2)
            if recv_msg.decode() == '1':
                # Get functionality
                self.client_get(conn)
            elif recv_msg.decode() == '2':
                self.uploadFile(conn)
            elif recv_msg.decode() == '3':
                self.server_settings(conn)
            elif recv_msg.decode() == '4':
                conn.send("Exiting...".encode())
            else:
                conn.send("Wrong choice entered!!".encode())
        else:
            print("Invalid username or password!!")
            conn.send("  ".encode())
