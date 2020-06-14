import os
import sys
import time
import getpass
from pathlib import Path


class FtsClient:
    logger = ""

    @staticmethod
    def get_user_details(s, threadcount, logger):
        # receive username entry
        logger = logger
        print(s.recv(1024).decode(), end="")
        username = input("")
        s.send((str(threadcount) + ":" + username).encode())
        # receive password entry
        print(s.recv(1024).decode(), end="")
        password = getpass.getpass(prompt="")
        s.send((str(threadcount) + ":" + password).encode('utf-8'))

    def get(self, s):
        filename = input('Enter Filepath(To exit, enter q): ')
        if filename != "q" and len(filename) > 0:
            s.send(filename.encode('utf-8'))
            data1 = s.recv(1024)
            data = data1.decode()
            if data[:6] == 'EXISTS':
                filesize = int(data[6:])
                message = input("File Exists, " + str(filesize) + "Bytes, download? Y/N> ->")
                if message == 'Y':
                    s.send(bytes('OK', 'utf-8'))
                    filename1 = filename[str(filename).rfind("/"):]
                    final_directory = str(Path(os.getcwd()).parent) + "\Downloads"
                    if not os.path.exists(final_directory):
                        os.makedirs(final_directory)
                    f = open(str(Path(os.getcwd()).parent) + "\Downloads\\" + filename1, 'wb')
                    data = s.recv(1024)
                    total_recv = len(data)
                    f.write(data)
                    while total_recv < filesize:
                        data = s.recv(1024)
                        total_recv += len(data)
                        f.write(data)
                    print("\033[1;32;40m")  # green color
                    print("Download complete")
                    print("\033[0;37;40m")  # normal text

                else:
                    print("\033[1;31;40m")  # red color
                    print("Download aborted")
                    print("\033[0;37;40m")  # normal text
            else:
                print("\033[1;31;40m")  # red color
                print("File does not exists!")
                print("\033[0;37;40m")  # normal text
        else:
            print("\033[1;31;40m")  # red color
            print("User Exited or no filename entered....")
            print("\033[0;37;40m")  # normal text

    def fts_put(self, s):
        filename = input('Enter FilePath (To exit, enter q): ')
        if len(filename) > 0 and filename != "q":
            s.send(filename.encode())
            if os.path.isfile(filename):
                concatwithSize = str(filename + ' EXISTS ' + str(os.path.getsize(filename)))
                print(concatwithSize)
                filenameAndSize = bytes(concatwithSize, 'utf-8')
                s.send(filenameAndSize)
                filepath = input('Enter the path where you want to upload the file: ')
                if len(filepath) > 0:
                    filepathBytecode = bytes(filepath, 'utf-8')
                    s.sendall(filepathBytecode)
                    if not (os.path.exists(filepath)):
                        file_path = s.recv(1024).decode()
                        print(file_path)
                    else:
                        with open(filename, 'rb') as f:
                            bytes_to_send = f.read()
                            s.send(bytes_to_send)
                        print(s.recv(1024).decode())
                else:
                    print("\033[1;31;40m")  # red color
                    print("no file path entered")
                    print("\033[0;37;40m")  # normal text


            else:
                file_path = s.recv(1024).decode()
                print(file_path)
        else:
            print("\033[1;31;40m")  # red color
            print("No filename given or user wants to quit")
            print("\033[0;37;40m")  # normal text
            sys.exit(1)

    def admin_settings_client(self, s, threadcount, logger):
        msg = s.recv(1024).decode()
        print(msg, end="")
        ch_inp = input("")
        s.send(ch_inp.encode())
        time.sleep(2)
        os.system("cls")
        if ch_inp == '1':
            print(s.recv(1024).decode())
            s.close()
        elif ch_inp == '2':
            print("\033[1;32;40m")  # green color
            print("List of users".center(os.get_terminal_size().columns))
            print("\033[0;37;40m")  # normal text
            test_string = s.recv(1024).decode()
            split_str = test_string.strip('[]').split(',')
            for i in range(len(split_str)):
                print(split_str[i])
            sys.exit(1)
        elif ch_inp == '3':
            print("\033[1;32;40m")  # green color
            print("Create new user".center(os.get_terminal_size().columns))
            print("\033[0;37;40m")  # normal text
            self.get_user_details(s, threadcount, self.logger)
            print(s.recv(1024).decode())
        elif ch_inp == '4':
            print("\033[1;32;40m")  # green color
            print("Remove user".center(os.get_terminal_size().columns))
            print("\033[0;37;40m")  # normal text
            print(s.recv(1024).decode(), end="")
            username = input("")
            s.send((str(threadcount) + ":" + username).encode())
            print(s.recv(1024).decode())
        else:
            print("\033[1;31;40m")  # red color
            print(s.recv(1024).decode())
            print("\033[0;37;40m")  # normal text

    def fts_client(self, s, threadcount, logger, pass_try_count):
        self.logger = logger
        if pass_try_count == 0:
            print("You Have Exceeded the Password Limit.Please Try After SomeTime!!!")
            sys.exit(0)
        self.get_user_details(s, threadcount, logger)
        recv_msg = s.recv(1024).decode()
        print("\033[1;32;40m")  # green color
        if recv_msg != 'Admin Settings':
            print(recv_msg)
        print("\033[0;37;40m")  # normal text
        self.logger.info(recv_msg)
        time.sleep(2)
        os.system("cls")
        if recv_msg == 'Admin Settings':
            print("\033[1;32;40m")  # green color
            print("Admin Settings!!\n".center(os.get_terminal_size().columns))
            print("\033[0;37;40m")  # normal text
            self.admin_settings_client(s, threadcount, logger)
        elif recv_msg == 'User Authenticated':
            print("\033[1;32;40m")  # green color
            print("Services for File Transfer\n".center(os.get_terminal_size().columns))
            print("\033[0;37;40m")  # normal text
            print(s.recv(1024).decode(), end="")
            msg2 = input("")
            s.send((str(threadcount) + ":" + msg2).encode())
            choice_rec = s.recv(1024).decode()
            time.sleep(2)
            os.system("cls")
            if choice_rec == '1':
                print("\033[1;32;40m")  # green color
                print("Get file from Server".center(os.get_terminal_size().columns))
                print("\033[0;37;40m")  # normal text
                self.get(s)
            elif choice_rec == '2':
                print("\033[1;32;40m")  # green color
                print("Put file to Server".center(os.get_terminal_size().columns))
                print("\033[0;37;40m")  # normal text
                self.fts_put(s)
            elif choice_rec == '3':
                print("\033[1;32;40m")  # green color
                print("Settings Options".center(os.get_terminal_size().columns))
                print("\033[0;37;40m")  # normal text
                self.client_settings(s, threadcount)
            elif choice_rec == '4':
                print("\033[1;31;40m")  # red color
                print(s.recv(1024).decode())
                print("\033[0;37;40m")  # normal text
                sys.exit(1)
            else:
                print("\033[1;31;40m")  # red color
                print(s.recv(1024).decode())
                print("\033[0;37;40m")  # normal text
                sys.exit(1)
        else:
            while pass_try_count > 0:
                return self.fts_client(s, threadcount, logger, pass_try_count - 1)

    def client_settings(self, s, threadcount):
        print(s.recv(1024).decode(), end="")
        choice_msg = input("")
        s.send((str(threadcount) + ":" + choice_msg).encode())
        if choice_msg == '1':
            print("\033[1;32;40m")  # green color
            print("View Logging\n".center(os.get_terminal_size().columns))
            print("\033[0;37;40m")  # normal text
            self.viewLogs(threadcount)
            sys.exit(1)
        elif choice_msg == '2':
            print("\033[1;32;40m")  # green color
            print("Add new User:\n".center(os.get_terminal_size().columns))
            print("\033[0;37;40m")  # normal text
            self.get_user_details(s, threadcount, self.logger)
            print(s.recv(1024).decode())
        else:
            print("\033[1;31;40m")  # red color
            print(s.recv(1024).decode())
            print("\033[0;37;40m")  # normal text
            sys.exit(1)

    def viewLogs(self, threadcount):
        logsFolderPath = str(Path(os.getcwd()).parent) + "\Logs\\"
        file = open(logsFolderPath + "Client" + str(threadcount) + ".log", "r")
        allContent = file.read()
        print(allContent)
        file.close()
