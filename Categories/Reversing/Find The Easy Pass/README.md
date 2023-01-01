# Find The Easy Pass
> Write-up author: jon-brandy
## DESCRIPTION:
Find the password (say PASS) and enter the flag in the form HTB{PASS}
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209571680-9ab030e2-de13-4158-a429-74c44065f6d2.png)


2. Let's decompile the `.exe` in ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210161971-f11b35f7-d086-4600-9543-1a2be62deea2.png)


3. Well we have many functions available, it's harder for us to do static reverse engineering.
4. So i used **Immunity Debugger**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210161993-6e027a62-9258-4204-9c8f-d48490eb5615.png)


5. Let's search for strings.

![image](https://user-images.githubusercontent.com/70703371/210162015-a87df46a-ad9f-4c7c-a906-e44fa2d1d639.png)


6. Let's take a look on this one.

![image](https://user-images.githubusercontent.com/70703371/210162027-261bb711-02aa-4dec-8e91-6a6560e6957a.png)


7. Let's set a breakpoint at this offset by press `f2`, then run the program.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210162069-9c906036-c9cf-4f60-80eb-9eb7aa949cd9.png)


![image](https://user-images.githubusercontent.com/70703371/210162075-5de9b0a8-36aa-407b-b652-6f0cb96cdb9f.png)


8. Now we know the correct pass is `fortran!`
9. Let's run it again but delete the breakpoint first, then enter the pass as `fortran!`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210162107-2d05bfcf-6bd0-4522-b549-5ec58fc4f0d8.png)


10. Got it correctly, hence we got the flag!

## FLAG

```
HTB{fortran!}
```

