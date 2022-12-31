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
