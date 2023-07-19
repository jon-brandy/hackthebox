# Anti Flag
> Write-up author: jon-brandy
## DESCRIPTION:
Flag? What's a flag?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Next, check type of file we got.

> RESULT - ELF 64 bit - Stripped

![image](https://user-images.githubusercontent.com/70703371/211237597-2b2d6e2c-0f42-4ac0-8d82-c84f6c84e9d5.png)


3. Run the binary.

![image](https://user-images.githubusercontent.com/70703371/211237788-ebc7a30e-806e-4606-b12c-fbbefe5079ff.png)


4. Hmm.. Let's decompile the binary.
5. Looks like i found the main function.

![image](https://user-images.githubusercontent.com/70703371/211238090-4f1d1099-f3f7-4b13-824e-857f2f1a2d22.png)


6. Found something that could be our interest.


![image](https://user-images.githubusercontent.com/70703371/211238385-f657f8fc-f81c-45c0-969e-4b94773c03b5.png)


![image](https://user-images.githubusercontent.com/70703371/211238497-7a0331db-6544-4732-91cd-6a6adf018fc2.png)


7. Could be this is an encrypted flag??

![image](https://user-images.githubusercontent.com/70703371/211238563-ed23044e-2845-4cc9-9f92-d65ebbe150a4.png)


8. And this is the key?

![image](https://user-images.githubusercontent.com/70703371/211238602-2aef5bf4-2c6c-45c1-8e21-23427c0ab91d.png)


9. But i don't know what encryption algorithm used.
10. Let's user another approach with patching the binary.
11. After analyzing the `main()` function, actually we can change the intruction for this offset to `jmp` to `0x1525`.

![image](https://user-images.githubusercontent.com/70703371/211239501-ba79843d-9fad-4a50-87e0-c81e038c5a32.png)


> RESULT - 0x1525

![image](https://user-images.githubusercontent.com/70703371/211240588-28177c1f-8218-4baf-819f-b26e70ed8bf6.png)


![image](https://user-images.githubusercontent.com/70703371/211240605-bbb43444-45f5-4c94-9df6-6b5d33c2992e.png)


12. Now export the binary and run it.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/211240665-2fced430-5c69-4a90-a756-4b23de71a545.png)


13. Got the flag!


## FLAG

```
HTB{y0u_trac3_m3_g00d!!!}
```

## ALTERNATE SOLUTION

1. Also we can solve it dynamically with gdb.
2. As we know the binary protection for PIE is enabled.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/df6ac9a8-8356-4087-8a67-c8ba2fb03b2c)


3. So to solve it dynamically we need to identify the piebase to do a jump (dynamically).
4. Before that i realize ghidra removes **uncreachable code** which we can undo that by doing this at ghidra:

```
edit -> tool options -> analysis -> "do uncheck" for eliminate reachable code
```

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/d493dfc1-fdbc-420a-b700-4c994b578297)


5. Then click apply.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/fdf72929-cc74-4a1d-8392-9e11f5440046)


6. As you can see we got another logic validations at the middle, which we can bypass by simply change to true, then we can get the flag easily (for static).
7. For dynamic, since the binary is stripped, we can't just set a breakpoint there:

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/2298d8bf-8964-49ac-a8f9-222579a7a74c)


8. Because we don't now the base address for the offset we want and we can't see the address.
9. But we can start breakpoint by ran `starti`. With this we can jump to the flag decode function to get the flag.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/208051f1-88b5-41b6-a842-1fb724e5439f)


> OUR INTEREST OFFSET TO JUMP (THE FLAG DECODE FUNCTION) --> 0x1525

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/8dcf22f1-50e1-4072-8c12-8bae34f534b4)


10. We can run `piebase 0x1525` to get the piebase for that offset then jump to the piebase we got.
11. But we can't just do that, it shall gave us **SEGMENTATION FAULT**.
12. We need to breakrva first at the first check (first if statement), then hit continue and grab the piebase for 0x1525 to jump there.

> SET BREAKPOINT AT 0x14f4 (first breakpoint) and hti continue

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/e988fe50-c90c-40d0-923d-1aad7249cd3b)


![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/9e8d3fc1-be2a-4a8d-93b0-64c590e5ad69)

> HIT CONTINUE

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/715751a8-6d3a-45a5-93fa-acaca818c655)


> GET PIEBASE for 0x1525 and JUMP there.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/7d2f7213-f902-45ff-8053-abd33e53178d)


13. Got the flag!



