import decimal
from decimal import Decimal
import random
import sympy
from sympy import *

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
    c = pow(input,e)
    ct = c % n
    return ct

def decryptVal(input,d,n):
    dtxt = Decimal(0)
    dtxt = pow(input,d)
    dt = dtxt % n
    return dt

def cText(arr,e,n):
    ret = []
    for i in arr:
        cv = cipherVal(i,e,n)
        ret.append(cv)
    return ret

def dText(arr,d,n):
    ret = []
    for i in arr:
        dv = decryptVal(i,d,n)
        ret.append(dv)
    return ret

#Generate Public Key
theNum1 = generateRandomPrimeDigit(0,100)
theNum2 = generateRandomPrimeDigit(0,100)
n = theNum1 * theNum2
t = (theNum1-1) * (theNum2-1) #phi(n)
e = generateExpNumber(t)

#Generating Private Key
d = generatePK(t,e)

#ciphered text
ecypTxt = cipherVal(1234,e,n)

#deciphered text
decypTxt = decryptVal(ecypTxt,d,n)

#print('p = '+str(theNum1)+' q = '+str(theNum2)+' n = '+str(n)+' t = '+str(t)+' e = '+str(e)+' d = '+str(d))
#print('ciphered text from 1234 is '+str(ecypTxt)+' and it shall pass be deciphered to '+str(decypTxt))

text = "Hello"
etxt = textEncode(text)
dlv = cText(etxt,e,n)
#transmitting >>>>>
dtxt = dText(dlv,d,n)
result = textDecode(dtxt)
print(text)
print(etxt)
print(dlv)
print(dtxt)
print(result)
