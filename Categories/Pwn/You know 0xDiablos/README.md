# You know 0xDiablos
> Write-up author: jon-brandy
## DESCRIPTION:
I missed my flag

## HINT:
- NONE
## STEPS:
1. First unzip the file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207644786-2b71a2bc-31f0-41b8-a85e-cd0c08f73f45.png)


2. Let's try to unzip it using `7z`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207645014-3ceb1439-e40d-401c-9bac-cf5ff74e6319.png)


3. Check the file type and the binary's protection.

> FILE TYPE

![image](https://user-images.githubusercontent.com/70703371/207645137-32ecbc90-2592-4b19-b6df-dd9f5df8ce9f.png)


```
32 Bit file, dynamically linked and not stripped.
```

> FILE'S PROTECTION

![image](https://user-images.githubusercontent.com/70703371/207645250-d4f9fb33-affa-423e-9ced-5d3e598f6897.png)


4. Now let's make the file executeable first by run `chmod +x vuln`, then run the file.

> INPUT ANY LENGTH OF A'S - RESULT

![image](https://user-images.githubusercontent.com/70703371/207646431-c05472b6-a7a9-4d81-b232-86bf038355c9.png)


5. As we know, since there's **no canary found**, then we can overflow the buffer.
6. I opened GDB and copied 1024 cyclic pattern, then run the file.

> GDB

![image](https://user-images.githubusercontent.com/70703371/207648015-176a3305-6214-49c3-93e5-1b13789cd213.png)


![image](https://user-images.githubusercontent.com/70703371/207648543-ac71b49a-166f-4bb2-801a-5b79be6a2c2b.png)


7. Copy the 4 chars in **EIP** , then do `cyclic -l waab`

```
EIP stands for Extended Instruction Pointer.
```

![image](https://user-images.githubusercontent.com/70703371/207649036-6d15d6e0-d67f-4ff3-813a-5594fa0f3660.png)


![image](https://user-images.githubusercontent.com/70703371/207649107-2487380c-4c9c-48ff-b372-032d07887552.png)


8. Now we know, we need to add 188 bytes as the padding.
9. Next, let's decompile the binary using ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207650199-f2fbdcf8-f495-478a-af85-edf6cbd5b5cb.png)


10. Check the `flag()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207650433-f2e6fe7e-7228-4f7c-829f-2c9ed0468f99.png)


11. 

