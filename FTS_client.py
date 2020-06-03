import sys


class FtsClient:

    @staticmethod
    def get_user_details(s):
        # receive username entry
        print(s.recv(1024).decode())
        username = input("")
        s.send(username.encode())
        print("Username received to Server:", s.recv(1024).decode())

        # receive password entry
        print(s.recv(1024).decode())
        password = input("")
        s.send(password.encode())
        print("Password received to Server:", s.recv(1024).decode())

    def fts_client(self, s):
        self.get_user_details(s)
        recv_msg = s.recv(1024).decode()
        print(recv_msg)
        if recv_msg == 'User Authenticated':
            print("=======Received FTP msg from server:=====")
            print(s.recv(1024).decode())
            msg2 = input("")
            s.send(msg2.encode())
            choice_rec = s.recv(1024).decode()
            print("====Received credentials message ====")
            if choice_rec == '1':
                   # TO DO: Add get functionality
                pass
            elif choice_rec == '2':
                    # TO DO: Add put functionality
                pass
            elif choice_rec == '3':
                print("client in")
                self.client_settings(s)
            else:
                print(s.recv(1024).decode())
                sys.exit(1)
        else:
            sys.exit(1)

    def client_settings(self, s):
        print(s.recv(1024).decode())
        s.send(input("").encode())
        rec_msg = s.recv(1024).decode()
        print(rec_msg)
        if rec_msg == '1':
            # TO DO: Add View logging
            pass
        elif rec_msg == '2':
            self.get_user_details(s)
            print("Data received from server:", s.recv(1024).decode())
        else:
            print(s.recv(1024).decode())
            sys.exit(1)


