# xorxorxor
> Write-up author: jon-brandy
## DESCRIPTION:
Who needs AES when you have XOR?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208122348-23590bfc-7eed-4f1f-8f7f-4baa31ba311c.png)


2. Strings the `.txt` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208122478-10fe8551-f567-45ea-85c1-0236d51680c7.png)


3. It must be the encrypted flag.
4. Now let's analyze the python code.

> RESULT

```py
#!/usr/bin/python3
import os
flag = open('flag.txt', 'r').read().strip().encode()

class XOR:
    def __init__(self):
        self.key = os.urandom(4)
    def encrypt(self, data: bytes) -> bytes:
        xored = b''
        for i in range(len(data)):
            xored += bytes([data[i] ^ self.key[i % len(self.key)]])
        return xored
    def decrypt(self, data: bytes) -> bytes:
        return self.encrypt(data)

def main():
    global flag
    crypto = XOR()
    print ('Flag:', crypto.encrypt(flag).hex())

if __name__ == '__main__':
    main()

```
