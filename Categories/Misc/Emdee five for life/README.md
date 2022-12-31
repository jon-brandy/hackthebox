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
3. For the first solution i tried to use python script.

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

## WITH BURPSUITE SOLUTION

1. Open the burpsuite, set the intercept to on, refresh the page, then send the request to intruder.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210124709-b68c0061-ca8d-4b8d-ba1c-02823fda62ce.png)


2. Choose the `clear` button.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210124713-7e4970d9-5cbe-44b9-b355-8bf51eb862fe.png)


3. Since we want to bruteforce the hash value, clear the hash value and add 2 `$$` dollar signs.
4. And add any character between the dollar signs as the **initial value**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210124732-0995c34d-539d-45e5-bc59-288d24b8753b.png)


5. Now open the payload tab.
6. Change the payload type to `recursive grep`.
7. Now open the options tab and scroll down to the `Grep Extract section`.

![image](https://user-images.githubusercontent.com/70703371/210124760-93623480-4dae-44ee-bcde-b1d0d86c7911.png)

> Check this one

![image](https://user-images.githubusercontent.com/70703371/210124777-ca724b4a-0b08-4db4-aa0a-0f18e0a1c700.png)


8. Then click the add button, copy this line:



