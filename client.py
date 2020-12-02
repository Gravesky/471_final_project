import socket
import sys
import select


HDR_LENGTH = 8
host = 'localhost'
port = 1989

# Setting the client name
clientName = input ("Please enter your name for the chatroom: ")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creation success at client side")
except socket.error:
    print("Socket creation failed at client side")

sock.connect((host, port))

# Set recv() to be non-blocking if there are no input
sock.setblocking(False)

cid = clientName.encode()
cid_length = len(cid)
client_hdr = "{cid_len:<{hdr_len}}".format(cid_len=cid_length, hdr_len = HDR_LENGTH).encode()
sock.send(client_hdr + cid)


print("<<<<<<<<<<<<<<<<<<< Welcome to this chat room >>>>>>>>>>>>>>>>>>>>>>")
print("<<<<<<<<<<<< Type words and press enter to send message >>>>>>>>>>>>")

#while (True):
    
#    recv_msg = sock.recv(1024)
#    print("Server: " + recv_msg.decode())
#    snd_msg = input()
#    sock.send( snd_msg.encode())
while (True):
    msg = input(clientName + ":")
    if msg:
        msg = msg.encode()
        msg_len = len(msg)
        msg_hdr = "{ml:<{hl}}".format(ml = msg_len, hl = HDR_LENGTH).encode()
        #msg_hdr = (str(msg_len) + ":<" + str(HDR_LENGTH)).encode()
        sock.send(msg_hdr + msg)
    try:
        while True:
            # Getting the header length and client name
            recv_header = sock.recv(HDR_LENGTH)
            if not len(recv_header):
                sys.exit()
            recv_length = int(recv_header.decode().strip())
            recvName = sock.recv(recv_length).decode()

            # Getting the message 
            msg_header = sock.recv(HDR_LENGTH)
            msg_length = int(msg_header.decode().strip())
            message = sock.recv(msg_length).decode()
                                 
            print(recvName+":"+message)

    # The non-blocking recv() cause IO exception when the client has not typed in any message
    # If it is the case that recv() is waiting, continue 
    except IOError:
        continue

sock.close()
