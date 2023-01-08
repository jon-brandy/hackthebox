# Ransom
> Write-up author: jon-brandy
## DESCRIPTION:
We received an email from Microsoft Support recommending that we apply a critical patch to our Windows servers. 
A system administrator downloaded the attachment from the email and ran it, and now all our company data is encrypted. Can you help us decrypt our files?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211203385-3c367240-5e4c-47b8-b454-c2cee37e3c49.png)


2. Hmm.. We got PE32+ file and encoded `.exe` file.
3. Let's decompile the PE32+ file.

> RESULT - MAIN FUNCTION


![image](https://user-images.githubusercontent.com/70703371/211203782-99e84329-a7a0-4822-8db2-44c150a10fea.png)


4. When i tried to check few functions, i found `encrypt` function and `encryptFile` function that could be our interest.


![image](https://user-images.githubusercontent.com/70703371/211205977-b2d4e2ea-c6d7-40ec-9da2-af2d124bd7bc.png)


![image](https://user-images.githubusercontent.com/70703371/211206090-abe7b431-3202-40c4-916b-60df4948ae37.png)


5. Notice when i tried to hover the `local_17` value. I got `CESREPUS` as characters.
6. Then for the `local_f` value in characters is `RU` and `local_d` value in character is `E`.
7. Concate all of them shall give us `ERUCESREPUS`.
8. Actually we can try to patch the loop here, so we can get the original decrypted file. But, i prefer use a python script to solve this challenge.
9. Before conduct the script, i tried to strings the excel file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211209459-d218a7ba-49d9-48ad-8c60-de27beb2ac91.png)


10. Hmm.. Looks like the text we got is reversed, remember it may stored in little endian. Hence the correct string is `SUPERSECURE`.
11. Let's make the script:

```py
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

```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/211210568-70aea9ce-320e-4bc9-a74b-1fc15d3c4fc9.png)


12. Copy all of it and paste it on cyberchef.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211210653-b08f4c23-10df-4c0a-af1c-e72bc600d621.png)


13. Got a clue here, based from it i think it's an excel file??

![image](https://user-images.githubusercontent.com/70703371/211210747-c664927f-f874-4a26-aade-e57ceaa0a69a.png)


14. Save the output to a file with `xlsx` extension.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211210788-15907d50-8e14-4835-9d55-20c10e89f542.png)


![image](https://user-images.githubusercontent.com/70703371/211210799-c15293f2-9793-4f04-ba15-fca9d6ccb65a.png)


15. Got the flag!


## FLAG

```
HTB{M4lW4R3_4n4LY5I5_IN73r357iN9_57uFF}
```

