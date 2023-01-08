from pwn import *
import os

os.system('clear')

key = list(b'SUPERSECURE')
encFile = read('login.xlsx.enc')

result = []
## applied the same concept as the for loop, but this time we substract it.
counter = 0
for i in encFile:
    result.append(i - key[counter % len(key)])
    counter += 1

flag = result
print(flag)
