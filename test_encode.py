import crypt

#Generate Public Key
theNum1 = crypt.generateRandomPrimeDigit(0,500)
theNum2 = crypt.generateRandomPrimeDigit(0,500)

theNum1 = int(input("p = "))
theNum2 = int(input("q = "))
n = theNum1 * theNum2
t = (theNum1-1) * (theNum2-1) #phi(n)
e = crypt.generateExpNumber(t)

#Generating Private Key
d = crypt.generatePK(t,e)
#When private key is less than 600, there tends to be a decipher error.
while(d < 600):
    d = crypt.generatePK(t,e)

# #ciphered text using public key
# ecypTxt = cipherVal(1234,e,n)

# #deciphered text using private key
# decypTxt = decryptVal(ecypTxt,d,n)

print('p = '+str(theNum1)+' q = '+str(theNum2)+' n = '+str(n)+' t = '+str(t)+' e = '+str(e)+' d = '+str(d))
# #print('ciphered text from 1234 is '+str(ecypTxt)+' and it shall pass be deciphered to '+str(decypTxt))

#text = "Hello"
text = str(input('Enter your message: '))
print(text)
#etxt = textEncode(text)
#text = text.encode()
#ctext = cipherVal(text,e,n)
dlv = crypt.cText(text,e,n)

str = crypt.listToStr(dlv)
print(str)
dstr = crypt.strToList(str)
print(dstr)
#transmitting >>>>>
dtxt = crypt.dText(dstr,d,n)
#result = textDecode(dtxt)

print(dtxt)
#print(dlv)
#print(dtxt)
#print(result)