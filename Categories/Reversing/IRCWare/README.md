# IRCWare
> Write-up author: jon-brandy
## DESCRIPTION:
During a routine check on our servers we found this suspicious binary, although when analyzing it we couldn't get it to do anything. We assume it's dead malware, but maybe something interesting can still be extracted from it?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Next check the type of file we got.

> RESULT - ELF 64 BIT, STRIPPED

![image](https://user-images.githubusercontent.com/70703371/212735370-4125c735-6f2b-422c-9ab6-db2990838f92.png)


3. Let's start by strings the binary to see if we can get any interesting clue here.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212735566-63bdfaa2-d58c-4684-8e34-d7723b00769e.png)


4. Got some IOC commands.
5. Let's decompil the binary then.
6. 
