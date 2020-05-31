import socket
from msslogger import MSSLogger

MSSLogger.intializelogger()
logger = MSSLogger.getlogger("clientlogger")
s = socket.socket()
host = "127.0.0.1"
port = 9999

s.connect((host, port))


def f_input():
    choice_msg = s.recv(1024)
    logger.info("======== Received choice message from server: =========\n "+ choice_msg.decode())
    print("======== Received choice message from server: =========\n ", choice_msg.decode())
    # User will provide the input as he wants to use the service
    choice_in = input("Please choose the functionality you want to proceed with: ")
    logger.info("Please choose the functionality you want to proceed with: "+choice_in)
    s.send(choice_in.encode())

    choice_rec = s.recv(1024)       # According to selected choice, look for the service
    logger.info(choice_rec.decode())
    
    if choice_rec.decode() == '1':
        echo_rcv = s.recv(1024).decode()
        print(echo_rcv)
        logger.info(echo_rcv)
        client_echo()

    elif choice_rec.decode() == '2':
        file_transfer()
    else:
        invalidoption()


def invalidoption():
    print("Oops !!! you have entered the wrong input\nDisconnecting from server \a...")
    logger.error("Oops !!! you have entered the wrong input\nDisconnecting from server \a...")


def client_echo():
    while True:
        msg = input("Enter the string: ")
        logger.info("Enter the string: "+msg)
        # send msg to server
        s.sendall(msg.encode())

        # echo reply from server
        data = s.recv(1024)
        print("Received echo message from server: ", data.decode())
        logger.info("Received echo message from server: "+data.decode())
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