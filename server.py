import socket
import sys
import select

HDR_LENGTH = 8
host = 'localhost'
port = 1989

# Creating Socket at Server Side
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #加了下面这一行可以重复使用地址
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket creation success at server")
except socket.error:
    print ("Socket creation error at server")

addr = (host, port)
sock.bind(addr)
print("Server socket binded to localhost and port #%s" %(port))

sock.listen()
print("Server socket is listening")

#下面这两段code是对应多个client的socket
sockets_list = [sock]


clients = {} # A list of client info that is stored in dictionary

#收到packet时，先读header，知道msg大小后，继续往后读
def recv_pkt(client_sock):
    try:

        pkt_hdr = client_sock.recv(HDR_LENGTH)

        if pkt_hdr is False:
            print("This client has close the connection.")
            return False

        payload = client_sock.recv(pkt_hdr)
        
        ret = {'HDR' : pkt_hdr, 'data' : payload}

        return ret
    
    except:
        print("This client has close the connection.")
        return False

while (True):

    # conn, address = sock.accept()
    # print("New incoming connection ")

    # while (True):
        
    #     recv_msg = conn.recv(1024)

    #     if (recv_msg.decode() == 'quit'):
    #         print("Client quit the chat")
    #         snd_msg = ("You have quit the chat")
    #         conn.send(snd_msg.encode())
    #         conn.close()
    #         break

    #     print("Client: " + recv_msg.decode())
    #     snd_msg = input()
    #     conn.send(snd_msg.encode())

    #下面都是我改（chao）的
    read_sock = select.select(sockets_list, [], sockets_list)

    for new_info_sock in read_sock:
        if new_info_sock != sock:
            #curently recieving packets/msg from one of the client 
            msg = recv_pkt(new_info_sock)

            if msg is False:
                print("Client"+ clients[new_info_sock]['data'].decode('utf-8') +"has close the connection.")
                sockets_list.remove(new_info_sock)
                del clients[new_info_sock]

                continue
            
            user = clients[new_info_sock]

            for client_sock in clients:
                if client_sock != new_info_sock:
                    #TODO ENCRYPTION REQUIRED
                    client_sock.send(user['HDR']+user['data']+msg['HDR']+msg['data'])
            
        else:
            #currently recieving packets from server (new connection)
            conn, address = sock.accept()
            
            user = recv_pkt(conn)

            if user is False:
                continue

            sockets_list.append(conn)

            clients[conn] = user

            print("New incoming connection at "+str(conn)+" : "+str(*address) + " from "+user['data'].decode('utf-8'))
#以上就是所有改动，直接借鉴吧，因为即使完全借鉴的话，我们最后还是要加入好多的东西（比如加密和UI），并且直接借鉴速度还快一点。











