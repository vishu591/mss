import socket

s = socket.socket()
host = "127.0.0.1"
port = 9999

s.connect((host, port))


def f_input():
    choice_msg = s.recv(1024)
    print("======== Received choice message from server: =========\n ", choice_msg.decode())
    # User will provide the input as he wants to use the service
    choice_in = input("Please choose the functionality you want to proceed with: ")
    s.send(choice_in.encode())

    choice_rec = s.recv(1024)       # According to selected choice, look for the service
    
    if choice_rec.decode() == '1':
        echo_rcv = s.recv(1024).decode()
        print(echo_rcv)
        client_echo()

    elif choice_rec.decode() == '2':
        file_transfer()

    else:
        Break()


def Break():
    print("Oops !!! you have entered the wrong input\nDisconnecting from server \a...")


def client_echo():
    while True:
        msg = input("Enter the string: ")
        # send msg to server
        s.sendall(msg.encode())

        # echo reply from server
        data = s.recv(1024)
        print("Received echo message from server: ", data.decode())
        if data.decode() == "Disconnecting from server ...\a":
            break
    s.close()


def file_transfer():
    print("Currently the code is under development ")
    pass                    # here FTS code will come


def main():
    f_input()


if __name__ == "__main__":
    main()