import socket
import sys
import threading
import time
import crypt
import tkinter as tk
import tkinter.font as ft

WAIT_TIME = 2.0
HDR_LENGTH = 8
host = 'localhost'
port = 1989

# def keyDump():
#     PubKexp
#     PubKnum
#     PrvKexp
#     PubKnum

#TODO Key sections

# Setting the client name
clientName = input ("Please enter your name for this chat session: ")
# Setting the contact name
recipientName = input ("Please enter the name of the person you wish to contact: ")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creation success at client side")
except socket.error:
    print("Socket creation failed at client side")

sock.connect((host, port))

# Set recv() to be non-blocking if there are no input
sock.setblocking(False)

#sending the client info
cid = clientName.encode()
cid_length = len(cid)
client_hdr = "{cid_len:<{hdr_len}}".format(cid_len=cid_length, hdr_len = HDR_LENGTH).encode()
sock.send(client_hdr + cid)
#sending the recipient info
rid = recipientName.encode()
rid_length = len(rid)
recipient_hdr = "{rid_len:<{hdr_len}}".format(rid_len=rid_length, hdr_len = HDR_LENGTH).encode()
sock.send(recipient_hdr+rid)

#Generating public key
theNum1 = crypt.generateRandomPrimeDigit(200,500)
theNum2 = crypt.generateRandomPrimeDigit(200,500)
n = theNum1 * theNum2
t = (theNum1-1) * (theNum2-1) #phi(n)
PrvKexp = crypt.generateExpNumber(t)

#TODO SEND PUBLIC KEY to recipitent. EXP & Num

#Sending Exp
kid = str(PrvKexp).encode()
kid_length = len(kid)
recipient_hdr = "{kid_len:<{hdr_len}}".format(kid_len=kid_length, hdr_len = HDR_LENGTH).encode()
sock.send(recipient_hdr+kid)

#Sending Num
kid = str(n).encode()
kid_length = len(kid)
recipient_hdr = "{kid_len:<{hdr_len}}".format(kid_len=kid_length, hdr_len = HDR_LENGTH).encode()
sock.send(recipient_hdr+kid)

#Generating Private Key
PrvKnum = crypt.generatePK(t,PrvKexp)
print("Private key = "+str(PrvKnum))
#When private key is less than 600, there tends to be a decipher error.
while(PrvKnum < 600):
    #print("Private key = "+str(PrvKnum))
    PrvKnum = crypt.generatePK(t,PrvKexp)

#TODO Get the public key from the sender
PubKexp = -1
PubKnum = -1
print("[CLIENT] Waiting to assign key...")
while(PubKexp == -1 or PubKnum == -1):

    try:
        if(PubKexp == -1):
            PubKexp_hdr = sock.recv(HDR_LENGTH)
            PubKexp_size = int(PubKexp_hdr.decode().strip())
            PubKexp = int(sock.recv(PubKexp_size).decode())
            print("[CLIENT] Public Exp key is assigned...")
        
        if(PubKnum == -1):
            PubKnum_hdr = sock.recv(HDR_LENGTH)
            PubKnum_size = int(PubKnum_hdr.decode().strip())
            PubKnum = int(sock.recv(PubKnum_size).decode())
            print("[CLIENT] Public Num key is assigned...")

    except BlockingIOError as e:
        #print("ERROR : "+str(e))
        time.sleep(5)

print("Recieved public keys are:\n exp = "+str(PubKexp)+" num = "+str(PubKnum))
    
#print('p = '+str(theNum1)+' q = '+str(theNum2)+' n = '+str(n)+' t = '+str(t)+' e = '+str(PrvKexp)+' d = '+str(PrvKnum))


def receive_display():
    # Display the received message on Chat screen
    while True:
        # Getting the header length and client name (From who)
        try:
            recv_header = sock.recv(HDR_LENGTH)
            if not len(recv_header):
                sys.exit()
            recv_length = int(recv_header.decode().strip())
            recvName = sock.recv(recv_length).decode()
            # Getting the message (Says what)
            #TODO add decryption
            msg_header = sock.recv(HDR_LENGTH)
            msg_length = int(msg_header.decode().strip())
            crypt_message = sock.recv(msg_length).decode()
            #print("[CLIENT] Ciphered Message recieved = "+crypt_message)
            #print("private key = "+str(PrvKnum)+" n = "+str(n))
            message = crypt.dText(crypt.strToList(crypt_message), PrvKnum, n)
            msg_box.insert(tk.END, recvName + ": " + message)
            print(recvName+":"+message)

        # The non-blocking recv() cause IO exception when the client has not typed in any message
        # If it is the case that recv() is waiting, break    
        except BlockingIOError:
            timer = threading.Timer(WAIT_TIME, receive_display)
            timer.start()
            break


def send_display(event = None):
    # Display the sent message on Chat screen
    orig_msg = tk_msg.get()
    msg_box.insert(tk.END, clientName + ": " + tk_msg.get())

    if orig_msg:
        #TODO add encryption
        #print("exp = "+str(PubKexp))
        msg = crypt.listToStr(crypt.cText(orig_msg,PubKexp, PubKnum))
        #print("[CLIENT] Ciphered Message sent = "+msg)
        msg = msg.encode()
        msg_len = len(msg)
        msg_hdr = "{ml:<{hl}}".format(ml = msg_len, hl = HDR_LENGTH).encode()
        #msg_hdr = (str(msg_len) + ":<" + str(HDR_LENGTH)).encode()
        sock.send(msg_hdr + msg)
        #AUTO-RECIEVE
        timer = threading.Timer(WAIT_TIME, receive_display)
        timer.start()
    
    tk_msg.set("")

# ========================================== tkinter UI Section ===========================================

# Setting the associated attributes for tkinter
chat = tk.Tk()
chat.title("Chat")

msg_frame = tk.Frame(chat)
scrollbar = tk.Scrollbar(msg_frame)

msg_font = ft.Font(family="Arial",size=12)
msg_box = tk.Listbox(msg_frame, height = 20, width = 75, yscrollcommand=scrollbar.set, font = msg_font)
msg_box.pack(side = tk.LEFT, fill = tk.BOTH)

msg_box.pack()
msg_frame.pack()

tk_msg = tk.StringVar()
tk_msg.set("Type Your Message Here")

entry_font = ft.Font(family="Arial",size=12,weight="bold")
input_entry = tk.Entry(chat, width = 50, textvariable = tk_msg, font = entry_font)
input_entry.bind("<Return>", send_display)
input_entry.pack()

sendButton = tk.Button(chat, text="Send", command=send_display, bg='darkcyan', fg='snow', width = 25)
sendButton['font'] = ft.Font(size = 12)
sendButton.pack(side = 'right')

refreshButton = tk.Button(chat, text = "Refresh", command = receive_display, bg = 'lightslategrey', fg = 'snow', width = 10)
refreshButton['font'] = ft.Font(size = 12)
refreshButton.pack(side = 'left')

msg_box.insert(tk.END, "<<<<<<<<<<<<<<<<<<<<<<<<<< Welcome <"+str(clientName)+"> to the Chatroom >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
msg_box.insert(tk.END, "<<<<<<<<<<<<<<<<<<<<< Type message and click 'Send' button >>>>>>>>>>>>>>>>>>>>>>>>>>")
#Initialize the auto-recieve
receive_display()

chat.mainloop()



# ===================================== End of Tkinter UI Section =========================================


#while (True):
        
#    #orig_msg = str(input(clientName + ":"))
#    orig_msg = tk_msg.get()
#    #send_display(clientName, orig_msg)
#    if orig_msg:
#        #TODO add encryption
#        #print("exp = "+str(PubKexp))
#        msg = crypt.listToStr(crypt.cText(orig_msg,PubKexp, PubKnum))
#        #print("[CLIENT] Ciphered Message sent = "+msg)
#        msg = msg.encode()
#        msg_len = len(msg)
#        msg_hdr = "{ml:<{hl}}".format(ml = msg_len, hl = HDR_LENGTH).encode()
#        #msg_hdr = (str(msg_len) + ":<" + str(HDR_LENGTH)).encode()
#        sock.send(msg_hdr + msg)
#    try:
#        while True:
#            # Getting the header length and client name (From who)
#            recv_header = sock.recv(HDR_LENGTH)
#            if not len(recv_header):
#                sys.exit()
#            recv_length = int(recv_header.decode().strip())
#            recvName = sock.recv(recv_length).decode()

#            # Getting the message (Says what)
#            #TODO add decryption
#            msg_header = sock.recv(HDR_LENGTH)
#            msg_length = int(msg_header.decode().strip())
#            crypt_message = sock.recv(msg_length).decode()
#            #print("[CLIENT] Ciphered Message recieved = "+crypt_message)
#            #print("private key = "+str(PrvKnum)+" n = "+str(n))
#            message = crypt.dText(crypt.strToList(crypt_message), PrvKnum, n)
#            receive_display(recvName, message)                     
#            print(recvName+":"+message)

#    # The non-blocking recv() cause IO exception when the client has not typed in any message
#    # If it is the case that recv() is waiting, continue 
#    except IOError:
#        continue


sock.close()
