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
4. Now let's analyze the python script.

> THE SCRIPT

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

5. Based from the script, we can conclude that each character will be XOR with each character of the key.
6. Not only that, we know that the length of the key is 4 characters.
7. We can assume that the 4 characters is `HTB{`.
8. If we xor the H with the 13 -> we got 5b

```
H in hex -> 48 (base16)
xor 48 with 13 -> 5b

T -> 54
xor 54 with 4a -> 1e

B -> 42
xor 42 with f6 -> b4

{ -> 7B
xor 7B with e1 -> 9a

I used this online tools to calculate the xor -> https://xor.pw/#

The key is -> 5b1eb49a

```

9. Next, i used [dcode.fr](https://www.dcode.fr/xor-cipher) for XOR BruteForce.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208127847-bbae34f1-7edd-402d-8a79-a46cc72827c3.png)


10. Got the flag!

## FLAG

```
HTB{rep34t3d_x0r_n0t_s0_s3cur3}
```
