# Blacksmith
> Write-up author: jon-brandy
## DESCRIPTION:
You are the only one who is capable of saving this town and bringing peace upon this land! 
You found a blacksmith who can create the most powerful weapon in the world! You can find him under the label "./flag.txt".
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209630413-478b7d78-09af-4f9c-adb6-5639252b1a44.png)


2. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209630465-9cf4b060-c9ec-44bd-9436-09c5ee7bf3fd.png)


3. Since it's a binary file, now check the the binary's protection.

> RESULT - NX DISABLED (Means we can inject shellcode and is allowed to execute it)

![image](https://user-images.githubusercontent.com/70703371/209630701-82e94e29-1116-4e00-b851-0ab925d72e7b.png)


4. Let's make the binary executeable by run `chmod` then run the binary file.

> RESULT

