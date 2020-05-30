import socket

def create_socket():
    """Socket Creation"""
    try:
        global host
        global port
        global s                #name of the socket
        host = ""               #this is the server file hence no host is required.
        port = 9999
        s = socket.socket()
    except  socket.error as msg:        #IN case connection timed out and socket craetion is failed.
        print ("Socket Creation error: " + str(msg))

def bind_scoket():
    """Binding the socket and listening for connection"""
    try:
        print ("Binding the port " + str(port))
        s.bind ((host, port))
        s.listen (5)

    except socket.error as msg:
        print("socket binding error: " + str (msg)+ "\n" + "Retrying ....") 
        bind_scoket()

def socket_accept():
    """Connection establishment with client"""
    conn,address = s.accept()
    print ("connection has been established " + "with IP " + address[0] + "and port " + str(address[1]))
    recv_data(conn)
    conn.close()

def recv_data(conn):
    choice_msg = "With which operation you would like to proceed with\n1.Echo\n2.File Transfer"
    conn.send(choice_msg.encode())
    choice = conn.recv(1024)
    print ("Service choosed is: ",choice.decode())
    conn.send(choice)

    if choice.decode() == "1":
        echo_strg = "you have chosed ECHO service !!!"
        conn.send(echo_strg.encode())
        server_echo(conn)
    if choice.decode() == "2":
        server_fts()

def server_echo(conn):
    while True:
        rcvdData = conn.recv(1024) 
        rcvdData1 = rcvdData.decode()
        print ("Input received from client: ", rcvdData1)
        if (rcvdData1 == "Quit" or rcvdData1 == "quit" or rcvdData1 == "Exit" or rcvdData1 == "exit"):
            conn.send("Disconnecting from server ...\a".encode())
            break
        conn.sendall(rcvdData)
    conn.close()

def server_fts():
    pass                    #function fot FTS code will come

def main():
    create_socket()
    bind_scoket()
    socket_accept()

if __name__ == "__main__":
    main()