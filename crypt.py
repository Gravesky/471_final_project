from decimal import Decimal
import random
from sympy import *
from sympy.plotting.plot import TextBackend

def textEncode(text):
    ctxt = []
    for char in text:
        ctxt.append(ord(char))
    return ctxt

def textDecode(arr):
    #print(arr)
    str = ""
    for i in arr:
        #print(i)
        str+=chr(i)
        #print(str)
    return str

def generateRandomPrimeDigit(p,q):
    primes = []
    for i in range(p,q):
        if(isprime(i)):
            primes.append(i)
    n = random.choice(primes)
    return n

def findExp(a,b):
    if b==0:
        return a
    else:
        return findExp(b,a%b)

def generateExpNumber(t):
    for e in range(2,t):
        if findExp(e,t)==1:
            return e

def generatePK(t,e):
    for i in range(1,10):
        k = 1+i*t
        if k % e == 0:
            d = int(k/e)
            return d

def cipherVal(input,e,n):
    c = Decimal(0)
    #print("[CRYPT][DEBUG] Decimal(0) = "+str(c)+" input = "+str(input)+" exp = "+str(e))
    c = pow(input,e)
    #print("[CRYPT][DEBUG] pow = "+str(c))
    ct = c % n
    #print("[CRYPT][DEBUG] ct = "+str(c))
    return ct

def decryptVal(input,d,n):
    dtxt = Decimal(0)
    dtxt = pow(input,d)
    dt = dtxt % n
    return dt

def cText(txt,e,n):
    arr = textEncode(txt)
    #print(arr)
    ret = []
    for i in arr:
        cv = cipherVal(i,e,n)
        #print(cv)
        ret.append(cv)
    return ret

def dText(arr,d,n):
    rarr = []
    for i in arr:
        dv = decryptVal(i,d,n)
        rarr.append(dv)

    #print("deciphered text encoded = "+str(rarr))
    ret = textDecode(rarr)
    return ret

def listToStr(list):
    ret = ' '.join([str(elem) for elem in list]) 
    return ret

def strToList(str):
    ret = []
    str_list = str.split()
    for num in str_list:
        ret.append(int(num))
    return ret



# #Generate Public Key
# theNum1 = generateRandomPrimeDigit(0,500)
# theNum2 = generateRandomPrimeDigit(0,500)
# n = theNum1 * theNum2
# t = (theNum1-1) * (theNum2-1) #phi(n)
# e = generateExpNumber(t)

# #Generating Private Key
# d = generatePK(t,e)
# #When private key is less than 600, there tends to be a decipher error.
# while(d < 600):
#     d = generatePK(t,e)

# # #ciphered text using public key
# # ecypTxt = cipherVal(1234,e,n)

# # #deciphered text using private key
# # decypTxt = decryptVal(ecypTxt,d,n)

# print('p = '+str(theNum1)+' q = '+str(theNum2)+' n = '+str(n)+' t = '+str(t)+' e = '+str(e)+' d = '+str(d))
# # #print('ciphered text from 1234 is '+str(ecypTxt)+' and it shall pass be deciphered to '+str(decypTxt))

# #text = "Hello"
# text = str(input('Enter your message: '))
# print(text)
# #etxt = textEncode(text)
# #text = text.encode()
# #ctext = cipherVal(text,e,n)
# dlv = cText(text,e,n)

# str = listToStr(dlv)
# print(str)
# dstr = strToList(str)
# print(dstr)
# #transmitting >>>>>
# dtxt = dText(dstr,d,n)
# #result = textDecode(dtxt)

# print(dtxt)
# #print(dlv)
# #print(dtxt)
# #print(result)

# # # Before send, we need to use the public key set to encrypt the data
# # # After recieve, we need to use the private key set to decrypt the data
