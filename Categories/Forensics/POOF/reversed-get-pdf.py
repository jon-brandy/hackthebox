from Crypto.Cipher import AES
from sys import exit
import random, string, time, os

os.system('clear')

## the decrypt function
def mv18jiVh6TJI9lzY(filename):
    data = open(filename, 'rb').read()
    key = 'vN0nb7ZshjAWiCzv'
    iv = b'ffTC776Wt59Qawe1' # must bytes
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv)
    ct = cipher.decrypt(data)
    Pkrr1fe0qmDD9nKx('new_boo', ct)

## to write out the output
def Pkrr1fe0qmDD9nKx(filename, data):
    open(filename, 'wb').write(data)
    #os.rename(filename, f"{filename}.boo")

mv18jiVh6TJI9lzY('candy_dungeon.pdf.boo')
