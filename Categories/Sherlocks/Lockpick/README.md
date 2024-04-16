# Lockpick

> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cf34454d-f333-4a0c-aa92-cb0d63b1cc1d)


## Lessons Learned:
- Conducting static malware analysis using ghidra.
- Reverse engineering C code-based Malware.

## SCENARIO:

<p align="justify">
  Forela needs your help! A whole portion of our UNIX servers have been hit with what we think is ransomware. We are refusing to pay the attackers and need you to find a way to recover the files provided. Warning This is a warning that this Sherlock includes software that is going to interact with your computer and files. This software has been intentionally included for educational purposes and is NOT intended to be executed or used otherwise. Always handle such files in isolated, controlled, and secure environments. One the Sherlock zip has been unzipped, you will find a DANGER.txt file. Please read this to proceed.
</p>

## STEPS:
1. In this challenge we're given 15 files.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/066c6ce2-ab48-4db5-93cf-68369107fc2e)


> 1ST QUESTION --> ANS: bhUlIshutrea98liOp

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0dadd44b-893c-4160-8feb-16f0f41bc8cc)


2. Reviewing the DANGER.txt file, we can conclude that the malware is inside the .zip file. This .txt file gives several warning upon analyzing the software and gave us the password for the zip file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/555669bc-772e-4908-9b73-28adcfe8dd26)


3. Unzipping it, we found the malware named --> `bescrypt3.2`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0d0ec4d9-84c6-45eb-9043-a62f87602db1)


4. To identify the encryption key used, I decompiled the binary using ghidra.
5. At the main() function, we can see a function named process_directory() is called, it have 2 parameters and both are strings.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cc293ba0-462d-4612-a9d1-74965e62666b)


6. Then analyzig the process_directory() function, we can tell that the second parameter is used again by another function named encrypt_file().

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/392168fd-8d31-4173-942e-10762ef9f502)


7. Reviewing the encrypt_file() code, it's clear that param2 is used as a key for XOR operation.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bdca4868-b1fc-4331-804a-b5acb5277bd2)


8. Hence it concludes that --> `bhUlIshutrea98liOp` is the key.

> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/037de062-cb14-49b6-acec-f329f522ba59)


9. To get his firstname and lastname, we just need to check the sql file of forela.
10. But sadly it's already encrypted by the malware.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f967784a-3ad0-4b2f-aeaa-fe581eae2e33)


11. Now we need to do malware reversing.
12. Upon reviewing all the functions available in the binary, seems our interest should be the `encrypt_file()` function.
13. The logic for the encryption lies at the XOR operation.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4fea2b1e-9bcd-4a6a-bcd8-a10e685ae734)


14. Hence, we just need to re-write the code focusing on this function. Things to note in XOR logic, if we XOR the encrypted data with the same key it used to encrypt, we shall retrieved the plaintext.
15. Remembering we already identified the key before, hence the rest should be just do the same operation again.
16. To decrypt the encrypted file I used python script.

> THE SCRIPT

```py
from pwn import *
import os
os.system('clear')

# function to grab all the encrypted files
def grab_encrypted(dir):
    files=[]
    for filename in os.listdir(dir): # enumerate every files inside the specified path
        if filename.endswith('.24bes'): # if it ends with .24bes, add it to our list.
            files.append(filename)
    return files

# function to decrypt the encrypted files.
def decrypt_files(path, file, output_directory):
    key = 'bhUlIshutrea98liOp' # param2
    key_length = len(key)

    output_path = os.path.join(output_directory, file[:-6]) # the slicing is to remove the .24bes name for the decrypted files.

    current_path = os.path.join(path, file) # current path

    with open(current_path, 'rb') as file:
        data_file = file.read()# read all the files inside the dir.
    
    file_content = bytearray()
    for i,y in enumerate(data_file):
        file_content.append(y ^ ord(key[i % key_length])) # DECRYPTING
    
    with open(output_path, 'wb') as f:
        f.write(file_content) # write the decrypted content to the output path

path = './' # current path
files = grab_encrypted(path) # grab all the encrypted files
output_directory = os.path.join(path, 'decrypted-files')
os.makedirs(output_directory) # create the output-dir

# decrypt each files
for i, file in enumerate(files, start=1):
    decrypt_files(path, file, output_directory)
    log.progress(f'IS DECRYPTING THE FILES')

log.success(f'DECRYPTION DONE')
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3a57b156-b220-49a2-a396-45ed0e6dcc28)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f4027aec-1470-49fa-ac6d-375cc0b042b9)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e7d29a43-4921-4291-98e2-f07e98477f1a)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ed700e63-c803-4c8e-a81b-79c4267a25bf)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/af68e25c-17ba-4a73-abaf-31200839d5f0)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ae8ecd3d-52bd-49f0-aa51-e0e7a7d5d112)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b4491f3-dd96-4e7c-9332-5e2cf76fc37b)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a7f1edf3-f4bc-4d08-8b61-2359d122dd19)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c715808a-aa2b-4a9f-aac4-68253139e943)


