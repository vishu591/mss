import os
import sys
from fileinput import filename
from pathlib import Path


class FtsClient:
    logger=""
    @staticmethod
    def get_user_details(s, threadcount, logger):
        # receive username entry
        logger =logger
        print(s.recv(1024).decode(), end="")
        username = input("")
        s.send((str(threadcount)+":"+username).encode())

        # receive password entry
        print(s.recv(1024).decode(), end="")
        password = input("")
        s.send((str(threadcount)+":"+password).encode('utf-8'))

    def get(self, s):
        filename = input('Enter FilePath(To exit, enter q): ')

        if filename != "q" and len(filename) > 0:
            print(filename)
            s.send(filename.encode('utf-8'))
            data1 = s.recv(1024)
            data = data1.decode()
            if data[:6] == 'EXISTS':
                filesize = int(data[6:])
                message = input("File Exists, " + str(filesize) + "Bytes, download? Y/N> ->")
                if message == 'Y':
                    s.send(bytes('OK', 'utf-8'))
                    filename1=filename[str(filename).rfind("/"):]
                    f = open(str(Path(os.getcwd()).parent)+"\Downloads\\"+ filename1, 'wb')
                    data = s.recv(1024)
                    total_recv = len(data)
                    f.write(data)
                    while total_recv < filesize:
                        data = s.recv(1024)
                        total_recv += len(data)
                        f.write(data)
                print("Download complete")
            else:
                print("File does not exists!")
        else:
            print("User Exited or no filename entered....")

    def fts_put(self, s):
        filename = input('Enter FilePath (To exit, enter q): ')
        if os.path.isfile(filename):
            if filename != "q":
                concatwithSize = str(filename + ' EXISTS ' + str(os.path.getsize(filename)))
                print (concatwithSize)
                filenameAndSize = bytes(concatwithSize, 'utf-8')
                s.send(filenameAndSize)
                filepath = input('Enter the path where you want to upload the file: ')
                filepathBytecode = bytes(filepath, 'utf-8')
                s.send(filepathBytecode)
                if os.path.exists(filepath):
                    with open(filename, 'rb') as f:
                        bytes_to_send = f.read()
                        s.send(bytes_to_send)
                    print(s.recv(1024).decode())
                else:
                    file_path = s.recv(1024).decode()
                    print (file_path)
            else:
                print("User Exited ...")
        else:
            print("No file name given or file not exists")

    def admin_settings(self, s):
        #     TODO:admin settings
        pass

    def fts_client(self, s,threadcount, logger):
        self.logger=logger
        self.get_user_details(s,threadcount,logger)
        recv_msg = s.recv(1024).decode()
        print(recv_msg)
        self.logger.info(recv_msg)
        if recv_msg == 'Admin Settings':
            self.admin_settings(s)
        elif recv_msg == 'User Authenticated':
            print(s.recv(1024).decode(), end="")
            msg2 = input("")
            s.send((str(threadcount)+":"+msg2).encode())
            choice_rec = s.recv(1024).decode()
            if choice_rec == '1':
                # get functionality
                self.get(s)
            elif choice_rec == '2':
                self.fts_put(s)
            elif choice_rec == '3':
                self.client_settings(s,threadcount)
            elif choice_rec == '4':
                print(s.recv(1024).decode())
                sys.exit(1)
            else:
                print(s.recv(1024).decode())
                sys.exit(1)
        else:
            sys.exit(1)

    def client_settings(self, s,threadcount):
        print(s.recv(1024).decode(), end="")
        choice_msg = input("")
        s.send((str(threadcount)+":"+choice_msg).encode())
        if choice_msg == '1':
            self.viewLogs(threadcount)
        elif choice_msg == '2':
            self.get_user_details(s, threadcount, self.logger)
            print(s.recv(1024).decode())
        else:
            print(s.recv(1024).decode())
            sys.exit(1)

    # This method is used to view client logs
    def viewLogs(self,threadcount):
        logsFolderPath=str(Path(os.getcwd()).parent)+"\Logs\\"
        file =open(logsFolderPath+"Client"+str(threadcount)+".log", "r")
        allContent=file.read()
        print(allContent)
        file.close()
