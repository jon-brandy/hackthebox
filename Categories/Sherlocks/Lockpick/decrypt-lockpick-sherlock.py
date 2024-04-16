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
