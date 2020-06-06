import sys


class FtsClient:

    @staticmethod
    def get_user_details(s):
        # receive username entry
        print(s.recv(1024).decode(), end="")
        username = input("")
        s.send(username.encode())

        # receive password entry
        print(s.recv(1024).decode(), end="")
        password = input("")
        s.send(password.encode('utf-8'))

    def get(self, s):
        filename = input('Enter Filename(To exit, enter q): ')
        print(filename)
        if filename != "q" and len(filename) > 0:
            s.send(filename.encode('utf-8'))
            data1 = s.recv(1024)
            data = data1.decode()
            if data[:6] == 'EXISTS':
                filesize = int(data[6:])
                message = input("File Exists, " + str(filesize) + "Bytes, download? Y/N> ->")
                if message == 'Y':
                    s.send(bytes('OK', 'utf-8'))
                    f = open('new_' + filename, 'wb')
                    data = s.recv(1024)
                    total_recv = len(data)
                    f.write(data)
                    while total_recv < filesize:
                        data = s.recv(1024)
                        total_recv += len(data)
                        f.write(data)
                        print("{0:.2f}".format((total_recv / float(filesize)) * 100) + "% Done")
                print("Download complete")
            else:
                print("File does not exists!")
        else:
            print("Enter proper filename")
        # s.close()

    def admin_settings(self, s):
        #     TODO:admin settings
        pass

    def fts_client(self, s):
        self.get_user_details(s)
        recv_msg = s.recv(1024).decode()
        print(recv_msg)
        if recv_msg == 'Admin Settings':
            self.admin_settings(s)
        elif recv_msg == 'User Authenticated':
            print(s.recv(1024).decode(), end="")
            msg2 = input("")
            s.send(msg2.encode())
            choice_rec = s.recv(1024).decode()
            if choice_rec == '1':
                # get functionality
                self.get(s)
            elif choice_rec == '2':
                # TO DO: Add put functionality
                pass
            elif choice_rec == '3':
                self.client_settings(s)
            elif choice_rec == '4':
                print(s.recv(1024).decode())
                sys.exit(1)
            else:
                print(s.recv(1024).decode())
                sys.exit(1)
        else:
            sys.exit(1)

    def client_settings(self, s):
        print(s.recv(1024).decode(), end="")
        choice_msg = input("")
        s.send(choice_msg.encode())

        if choice_msg == '1':
            # TO DO: Add View logging
            pass
        elif choice_msg == '2':
            self.get_user_details(s)
            print(s.recv(1024).decode())
        else:
            print(s.recv(1024).decode())
            sys.exit(1)
