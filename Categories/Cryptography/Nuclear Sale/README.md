# Nuclear Sale
> Write-up author: jon-brandy
## DESCRIPTION:
Plutonium Labs is a private laboratory experimenting with plutonium products. A huge sale is going to take place and our intelligence agency is interested in learning more about it. We have managed to intercept the traffic of their mail server. Can you find anything interesting?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a pcap file.
2. At first i tried to ran strings to the file rather open it on wireshark.
3. Then found 3 things that could be our interest.

> ENCRYPTED INFORMATION

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/ebd774e2-78a7-4ec3-a30b-26b26b46f01c)


> 2 Ciphertext encrypted with unknown key

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/78629af5-620f-4a4c-a2d1-718d4228db9b)


4. Since i'm not a fond in crypto, kinda confused what to do, then i found a message that indicate a XOR operations (?)

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/c08a8066-8133-4972-8f92-d77bb0042b97)


5. Since all encrypted text are XORed with the same key, hence we can apply this:

```py
from pwn import * 

enc_info = '6b65813f4fe991efe2042f79988a3b2f2559d358e55f2fa373e53b1965b5bb2b175cf039'
cipher_1 = 'fd034c32294bfa6ab44a28892e75c4f24d8e71b41cfb9a81a634b90e6238443a813a3d34'
cipher_2 = 'de328f76159108f7653a5883decb8dec06b0fd9bc8d0dd7dade1f04836b8a07da20bfe70'

enc_bytes = unhex(enc_info)
cipher_1_bytes = unhex(cipher_1)
cipher_2_bytes = unhex(cipher_2)

#print(enc_bytes)
#print(cipher_1_bytes)
#print(cipher_2_bytes)

result = []
# [+] Decrypting starts here
for i, j in enumerate(enc_bytes):
    result.append(j ^ cipher_1_bytes[i] ^ cipher_2_bytes[i])

log.success(result)
flag = ""
for i in result:
    flag += chr(i)

log.success(flag)
```

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/cba4f7e8-603e-49b3-a6a9-6c34319ef424)


6. Got the flag!

## FLAG

```
HTB{s3cr3t_sh4r1ng_w1th_x0r_15_l4m3}
```
