import socket
import sys

host = 'localhost'
port = 1234

# Creating Socket at Server Side
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creation success at server")
except socket.error:
    print ("Socket creation error at server")

addr = (host, port)
sock.bind(addr)
print("Server socket binded to localhost and port #%s" %(port))

sock.listen(5)
print("Server socket is listening")

while (True):

    conn, address = sock.accept()
    print("New incoming connection ")

    while (True):
        
        recv_msg = conn.recv(1024)

        if (recv_msg.decode() == 'quit'):
            print("Client quit the chat")
            snd_msg = ("You have quit the chat")
            conn.send(snd_msg.encode())
            conn.close()
            break

        print("Client: " + recv_msg.decode())
        snd_msg = input()
        conn.send(snd_msg.encode())
    




