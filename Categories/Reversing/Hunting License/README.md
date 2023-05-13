# Hunting License
> Write-up author: vreshco
## DESCRIPTION:
STOP! Adventurer, have you got an up to date relic hunting license? If you don't, you'll need to take the exam again before you'll be allowed passage into the spacelanes!
## HINT:
- NONE
## STEPS:
1. Unzipping the zip file shall resulting to a 64 bit binary file.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/9d8c5b87-4ed4-4e88-a5ea-ffe52558ee60)

2. It's interesting, because in reversing we're rarely have a host to run in order to get the flag.
3. Let's run the host first to check what is it.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/254c1238-7c5b-49ee-a39a-b7660cbb3ab5)


4. Seems we need to answer all the questions in order to get the flag.
5. The first questions it asked about the file format.
6. Well we can check that simply by running `file license` and as you can see the format file is **ELF**.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/6250e97d-395b-4b87-b199-67679fa0d67a)


7. Now it's asking the CPU Architecture, based from the result of file command, it's **64 bit**.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/fe82fe98-a288-4541-8909-3e3be5f67cbb)

8. Let's run ldd to the binary -> `ldd license`. It's **libreadline.so.8**.


![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/0560f1ac-6801-4546-a1a7-00aeed02e8d7)


9. Great, now it's asking the address of the main() function.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/e38f93b7-959e-4bf7-a617-ffb1afb1762c)


> Using GDB

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/50217bf8-c669-4caa-8602-a77b4e139183)

10. It's **0x401172**.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/06ff3ddb-120c-46fc-9f9a-f719378a85a6)


11. Well we still can identify that by disassemble the main() function.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/c0e863ec-06d3-49e6-a0c5-e96b225d008a)


12. We have **5 puts@plt**.
13. Next, it's asking for the first password.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/6029b7bd-81c3-4d35-acdf-e5904d133453)


> Using GHIDRA 

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/62a1b234-ee9f-4960-8589-2aee665e6283)


14. To make sure we have the correct password, let's run the binary.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/24f8cfa6-fae6-4db9-8044-53636b36137b)


15. Got it correctly -> **PasswordNumeroUno**.
16. Next it's asking the reversed form of the 2nd password.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/5e819945-6dd3-44f7-8608-cdc2be838527)


17. Let's analyze the main() function.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/0b27198a-2457-40b1-a45c-20bac39397cf)


18. It seems the 2nd password is the result of the reverse() call.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/ecb91e4a-1d37-4b38-89fe-1cd916c4891f)


19. Since it will take time to do static analysis, let's do dynamic by set a breakpoint at the strcmp().

> Using GDB

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/08587e8e-f045-4b57-be26-fa6afa1dea02)


![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/b98f0418-136d-400a-920d-9ebd4b880cc0)


20. Now enter random text.
21. Great! We hit the breakpoint.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/175086f4-5ad8-4901-b9a8-c2c5536bcc3a)


![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/2539286d-ed4f-4f75-a786-fc8033b06484)


22. As you can see it's comparing our input to `P4ssw0rdTw0`. It must be the correct one, let's test that by use them.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/d2afcd1a-6a3a-438b-a8f8-14f2b3168657)


23. Got it correct!
24. To answer the question simply reverse it -> **0wTdr0wss4P**.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/88c71d8a-9f85-4ebb-8a0e-3e62a000f49f)


25. It's asking for the real one -> **P4ssw0rdTw0**.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/a04ef979-7628-4002-b464-3e26eff4caee)


26. It's asking for the key used to XOR. Let's open ghidra again.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/cf8c8806-7519-42bd-81d1-43715b1e8d47)


27. It using the 4th param as the key.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/666bd590-9de5-4048-bebd-bcdf42291e77)


28. It's 19 then.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/efcbdcef-cebe-4bc4-b718-0a38b8d34e98)


29. To get the 3rd password, simply do the same process by set a breakpoint at the comparing section.
30. Turns out it's -> **ThirdAndFinal!!!**

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/781addd7-56e9-4bed-b42f-1eef3e61f35d)

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/3c945ce1-e1f8-4741-be63-78e92927ab02)


31. Got the flag!

## FLAG

```
HTB{l1c3ns3_4cquir3d-hunt1ng_t1m3!}
```


