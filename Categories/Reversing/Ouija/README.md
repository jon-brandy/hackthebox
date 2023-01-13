# Ouija
> Write-up author: jon-brandy
## DESCRIPTION:
You've made contact with a spirit from beyond the grave! 
Unfortunately, they speak in an ancient tongue of flags, so you can't understand a word. 
You've enlisted a medium who can translate it, but they like to take their time...
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209523415-d553c94d-30f2-4f88-9358-db30bea5defb.png)


2. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209523457-0828d787-4030-420c-b352-fe0f0dd51e0c.png)


3. Great, it's not stripped. Hence it's easier for us to reverse the binary.
4. Let's run the binary in GDB.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209524134-2e042478-0c11-4b88-8b20-118f2437f3bc.png)

5. It stucks here (?)

![image](https://user-images.githubusercontent.com/70703371/209524215-ad496467-4bc2-44e9-a52e-219a1e5f3388.png)


6. Let's decompile the binary using ghidra and open the `main()` function.
7. Got the reason why the program took long enough to output a message.

![image](https://user-images.githubusercontent.com/70703371/209524377-51b05668-48b3-4587-9ed0-88d48f60598a.png)

![image](https://user-images.githubusercontent.com/70703371/209524406-6f486aec-aec4-4948-9b15-d9a489a2e1c7.png)


8. Well let's change every `sleep()` function's that say 10 to 0.

![image](https://user-images.githubusercontent.com/70703371/212287721-55bbf5db-25b7-45af-9934-75af525c7a4a.png)

9. Export the binary, make it executeable, now run the binary.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212292151-b63c6242-e92d-4c66-8a1a-70aa6a7a7bff.png)


![image](https://user-images.githubusercontent.com/70703371/212323240-290e7e20-eff7-4a29-98a8-d32719583a22.png)


10. As you can see, it starts to print out the flag.

## FLAG

```
HTB{Sleping_is_not_obfuscation}
```


