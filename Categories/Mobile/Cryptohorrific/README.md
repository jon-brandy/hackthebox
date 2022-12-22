# Cryptohorrific
> Write-up author: jon-brandy
## DESCRIPTION:
Secure coding is the keystone of the application security!
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given and jump to the extracted folder.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/209180387-f9685fbc-0e58-4447-b139-bf43139b54d0.png)


2. After checking every files, found one file that looks like have a base64 strings encoded inside. But actually it's not. 

> CHALLENGE.PLIST

![image](https://user-images.githubusercontent.com/70703371/209180762-63d0ab70-519a-4c98-b84c-bce5b5fc6355.png)


3. Based on the file's extension, we can conclude that we given an IOS mobile application.
4. Let's decompile the Mach-O 64-bit x86_64 executable file.

> HOPPER

