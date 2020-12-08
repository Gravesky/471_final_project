import socket
import crypt
import select

HDR_LENGTH = 8
host = 'localhost'
port = 1989

# Creating Socket at Server Side
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #To repeaetingly use the same address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket creation success at server")
except socket.error:
    print ("Socket creation error at server")

addr = (host, port)
sock.bind(addr)
print("Server socket binded to localhost and port #%s" %(port))

sock.listen()
print("Server socket is listening")

#For multi clients and sockets
sockets_list = [sock]

index = 1

clients = {} # A list of client info that is stored in dictionary

recievers = {} # A list of reciver candidate and their contact

recievers_conn = {} # A list of contact's socket index to the socket_list above

# A list of client public key info is stored
client_public_key_nums = {} 
client_public_key_exps = {}

# Sending server message to the client
def serverMessage(orig_msg):

    #prepare socket
    sender = clients[new_info_sock]
    sender_name = clients[new_info_sock]['data'].decode()
    reciever_name = recievers[sender_name]
    contact_sock_index = recievers_conn[reciever_name]
    contact_sock = sockets_list[contact_sock_index]

    #prepare public key for encryption
    PubKexp = int(client_public_key_exps[reciever_name].decode())
    PubKnum = int(client_public_key_nums[reciever_name].decode())
    print("pkexp = "+str(PubKexp)+" / pknum = "+str(PubKnum))
    print("The meesage is : "+str(orig_msg))
    #sending the meesage
    msg = crypt.listToStr(crypt.cText(orig_msg, PubKexp, PubKnum))
    #print("[CLIENT] Ciphered Message sent = "+msg)
    msg = msg.encode()
    msg_len = len(msg)
    msg_hdr = "{ml:<{hl}}".format(ml = msg_len, hl = HDR_LENGTH).encode()
    #msg_hdr = (str(msg_len) + ":<" + str(HDR_LENGTH)).encode()
    contact_sock.send(sender['HDR']+sender['data']+msg_hdr + msg)

#When recieved packets, read the header first, know the bytes number and then read the data
def recv_pkt(client_sock):
    try:
        print("[RECIEVE] RECIEVING from "+str(client_sock))
        pkt_hdr = client_sock.recv(HDR_LENGTH)
        
        if not len(pkt_hdr):
            print("[RECIEVE PKT] pkt_hdr is false")
            return False

        payload_length = int(pkt_hdr.decode().strip())
        print("[RECIEVE] Trying to recieve "+str(payload_length)+" bytes from socket")
        payload = client_sock.recv(payload_length)
        
        ret = {'HDR' : pkt_hdr, 'data' : payload}
        print("[RECIEVE] This packet -> "+str(ret))
        return ret
    
    except:
        
        print("recv_pkt exception")
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

    read_sock,write_sock, _ = select.select(sockets_list, [], sockets_list)

    for new_info_sock in read_sock:
        if new_info_sock != sock:
            print("<-------------------New Message------------------->")
            #curently recieving packets/msg from one of the client 

            msg = recv_pkt(new_info_sock)

            if msg is False:
                #TODO send server message to reciever telling the connection is off
                disconnect_txt = "[SERVER MESSAGE] Our Client <"+ str(clients[new_info_sock]['data'].decode()) +"> has close the connection."
                serverMessage(disconnect_txt)
                print("Client <"+ clients[new_info_sock]['data'].decode() +"> has close the connection.")
                sockets_list.remove(new_info_sock)
                del clients[new_info_sock]

                continue
            
            sender = clients[new_info_sock]
            sender_name = sender['data'].decode()
            reciever_name = recievers[sender_name]
            contact_sock_index = recievers_conn[reciever_name]
            contact_sock = sockets_list[contact_sock_index]

            print("[SERVER] Sending to socket : "+str(contact_sock))
            #TODO use index to find who to contact on which socket
            contact_sock.send(sender['HDR']+sender['data']+msg['HDR']+msg['data'])
            # for client_sock in clients:
            #     #find the right client and send the msg
            #     if client_sock == contact_sock:
            #         client_sock.send(sender['HDR']+sender['data']+msg['HDR']+msg['data'])
            print("[SERVER] Encrypted Message to <"+reciever_name+"> has been forwarded :\n"+str(msg['data'].decode()))
            
        else:
            print("<-------------Connection Established------------->")
            #currently recieving packets from server (new connection)
            conn, address = sock.accept()
            
            sender = recv_pkt(conn)
            reciever = recv_pkt(conn)
            public_key_exp = recv_pkt(conn)
            public_key_num = recv_pkt(conn)

            if sender is False:
                continue
            if reciever is False:
                continue
            if public_key_exp is False:
                continue
            if public_key_num is False:
                continue

            sockets_list.append(conn)
            clients[conn] = sender

            sender_name = sender['data'].decode()

            recievers_conn[sender_name] = index
            index = index + 1
            #print("[DEBUG] SAVED CONNECTION : "+)

            reciever_id = reciever['data'].decode()
            recievers[sender_name] = reciever_id

            client_public_key_exps[sender_name] = public_key_exp['data']

            client_public_key_nums[sender_name] = public_key_num['data']

            #check if existing contact in the list, so key excahnge can be finsihed.
            if(reciever_id in recievers):
                #find the correct public key and send to this current new cleint
                PKexp1 = client_public_key_exps[reciever_id]
                PKexp1_length = len(PKexp1)
                PKexp1_hdr = "{PKexp1_len:<{hdr_len}}".format(PKexp1_len=PKexp1_length, hdr_len = HDR_LENGTH).encode()
                conn.send(PKexp1_hdr+PKexp1)

                PKnum1 = client_public_key_nums[reciever_id]
                PKnum1_length = len(PKnum1)
                PKnum1_hdr = "{PKnum1_len:<{hdr_len}}".format(PKnum1_len=PKnum1_length, hdr_len = HDR_LENGTH).encode()
                conn.send(PKnum1_hdr+PKnum1)

                print("[SERVER] Public keys has been sent to "+sender_name)

                #send the public key of this current new client to its contact
                contact_sock_index = recievers_conn[reciever_id]
                print("sender is "+str(reciever_id)+"sock index at "+str(contact_sock_index))
                contact_sock = sockets_list[contact_sock_index]
                print("[SERVER] "+reciever_id+" 's socket = "+str(contact_sock))

                PKexp2 = client_public_key_exps[sender_name]
                PKexp2_length = len(PKexp2)
                PKexp2_hdr = "{PKexp2_len:<{hdr_len}}".format(PKexp2_len=PKexp2_length, hdr_len = HDR_LENGTH).encode()
                contact_sock.send(PKexp2_hdr+PKexp2)

                PKnum2 = client_public_key_nums[sender_name]
                PKnum2_length = len(PKnum2)
                PKnum2_hdr = "{PKnum2_len:<{hdr_len}}".format(PKnum2_len=PKnum2_length, hdr_len = HDR_LENGTH).encode()
                contact_sock.send(PKnum2_hdr+PKnum2)

                print("[SERVER] Public keys has been sent to "+reciever_id)

            print("New incoming connection at "+str(conn)+" : "+str(address) + " from "+sender['data'].decode()+" to "+reciever_id)
            print("Public Key Set: ")
            print("  EXP = "+str(public_key_exp))
            print("  NUM = "+str(public_key_num))