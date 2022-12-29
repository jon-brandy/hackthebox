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


4. Let's decompile the binary using ghidra.

> RESULT - MAIN FUNCTION

![image](https://user-images.githubusercontent.com/70703371/209918543-54eae053-c967-46a9-b0fc-94e07cb27295.png)


5. Based from the `main()` function, we know that the program will prompts us an input.
6. If we input 1, then the program will print `&DAT_001012e0`, which allows us to choose another input.

![image](https://user-images.githubusercontent.com/70703371/209918798-9988c6f5-1c2a-4d90-9510-a948e7a4a395.png)


7. If we choose 2, the program will call the `shield()` function, 3 for the `bow()` function and 1 for the `sword()` function.

![image](https://user-images.githubusercontent.com/70703371/209918965-f1009b6a-0b41-4683-b1c6-a1015d91228a.png)


8. Let's deep dive to those 3 functions.
9. 
