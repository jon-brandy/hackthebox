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

