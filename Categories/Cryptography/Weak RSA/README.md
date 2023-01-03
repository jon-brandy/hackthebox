# Weak RSA
> Write-up author: jon-brandy
## DESCRIPTION:
Can you decrypt the message and get the flag?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210298275-cb4a8303-d7c4-4de0-9010-e79a6002995f.png)


![image](https://user-images.githubusercontent.com/70703371/210298279-0b7800fd-6dd3-46d7-9cd4-83459f4ac1ed.png)


![image](https://user-images.githubusercontent.com/70703371/210298289-5c651bd9-0f15-4c84-a1bb-01bc967fe415.png)


2. For this solution i used `RsaCtfTool`.

> RESULT

```
./RsaCtfTool.py --publickey ./key.pub --uncipherfile ./flag.enc
```

![image](https://user-images.githubusercontent.com/70703371/210300823-ba38335b-e9a5-4bdf-b6ef-2029ae29260b.png)


3. Dunno why we didn't get any output, let's try another way by get the private key first and save it to a file named `key.pri`.

> GET THE PRIVATE KEY FIRST.

```
./RsaCtfTool.py --publickey ./key.pub --private
```

![image](https://user-images.githubusercontent.com/70703371/210300780-c9f433ae-0169-4b56-9f6a-93c28585cc8c.png)


4. To get the flag run this payload:

```sh
openssl pkeyutl -in flag.enc -out flag.txt -decrypt -inkey key.pri
```

![image](https://user-images.githubusercontent.com/70703371/210301088-acfbbd2b-0af2-4b88-b517-6eccf7b13dc9.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/210301103-788056b4-a779-49a7-b727-e75b6affcc1c.png)


5. Got the flag!

## FLAG

```
HTB{s1mpl3_Wi3n3rs_4tt4ck}
```
