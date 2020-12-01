import socket
import sys

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creation success at client side")
except socket.error:
    print("Socket creation failed at client side")

port = 1989
sock.connect(('localhost', port))

print("Welcome to this chat room")
print("Type words and press enter to send message")
print("Type quit and press enter to exit the connection")

while (True):
    snd_msg = input()
    sock.send( snd_msg.encode() )
    recv_msg = sock.recv(1024)

    print("Server: " + recv_msg.decode())

sock.close()
