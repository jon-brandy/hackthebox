# Emdee five for life
> Write-up author: jon-brandy
## DESCRIPTION:
Can you encrypt fast enough?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210124326-2147281e-b09a-494d-9d54-d8a3b1f58d67.png)


![image](https://user-images.githubusercontent.com/70703371/210124412-bcd6ca1e-e125-4007-9eb2-acb528ff111a.png)


2. What comes to my mind is we can use intruder in burpsuite to bruteforce the hash or we can use python script.
3. For this solution i tried to use python script.

> THE SCRIPT

```py
from pwn import *
import requests
import os
from bs4 import BeautifulSoup

os.system('clear')

context.log_level = 'debug'
url = 'http://142.93.37.215:30301/'
cookies = {'PHPSESSID': '9eddrh0aufnmjqpg8cpht98pb1'} # get the cookie value using burpsuite

response = requests.get(url, cookies=cookies)  # Initial request

# Loop until we see the HTB string
while 'HTB' not in response.text:
    # Since the hash is inside the <h3> tag, then we need to extract it using h3.contents
    # Then add [0], because we want just the value not all the <h3> tag
    extractString = BeautifulSoup(response.text, features="lxml").h3.contents[0]
    debug('extracted: %s', extractString)

    # MD5 the extracted string
    hashedString = md5sumhex(extractString.encode())
    debug('hash: %s', hashedString)

    # Submit the hash
    response = requests.post(url, data={'hash': hashedString}, cookies=cookies)

# Print the response if we got the HTB string
extracted = BeautifulSoup(response.text, features="lxml").p.contents[0]
warn(extracted)
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/210124609-9b07cfa5-a6dd-4a21-8164-ab8b56865b16.png)


4. Got the flag!

## FLAG

```
HTB{N1c3_ScrIpt1nG_B0i!}
```
