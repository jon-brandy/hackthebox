# Assemblers Avenge

> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/54ad889e-0ed2-4f15-892d-06264bd8d2ad)

# Lessons Learned:
- ret2shellcode.
- create custom shellcode.
- utilize `/bin/sh` strings printed.

## DESCRIPTION:

<p align="justify">Amidst the harrowing conflict, our city bore the brunt of relentless onslaughts, witnessing widespread devastation that spared little, ravaging both infrastructure and spirit alike. Now, as the dust settles and the echoes of chaos fade, a clarion call emerges: assemble a force to restore justice and herald a new era of tranquility. With the remnants of our past preserved within this binary, embark on your mission to reclaim our future. </p>

## STEPS:
1. In this challenge we are given a 64 bit binary, statically linked, and not stripped.

![image](https://github.com/user-attachments/assets/53c72f0e-8586-4923-af2b-b6011344c919)


> BINARY PROTECTIONS

![image](https://github.com/user-attachments/assets/a508e2de-1f69-414d-a4cc-b13c2bf9507b)

2. Since it is statically linked, hence the binary does not rely on external shared libraries during runtime.
3. Also notice that all the binary mitigations are off, should be easy to pwn then.
4. Decompiled the binary at ghidra and reviewed the entry, we identified three functions called, those are **_write**, **_read**, and **_exit**.

> Ghidra

![image](https://github.com/user-attachments/assets/ea12e6ab-34cd-4cb8-9c87-c96044d2dad6)

5. Reviewing the **_write** call operations, we can see what message shall be printed.

![image](https://github.com/user-attachments/assets/4a9f1b9b-20f9-48ca-b43c-55fd5015e433)

![image](https://github.com/user-attachments/assets/a4701a42-c92e-4835-9f2b-3ad25f351647)


6. Reviewing the **_read** function call, we can identify the buffer size (**_nbytes**) is 24 bytes.

![image](https://github.com/user-attachments/assets/c0755bb1-2273-42d5-9747-a7dd75d22908)

7. If you noticed, our input shall stored at RSI at this function call, which gave us a hint to utilize `jmp` instruction to rsi if we use shellcode approach.

![image](https://github.com/user-attachments/assets/60b96fbe-e6ec-4883-a53b-43c96f5d3d8f)


8. For the **_exit** function call, it just printed the goodbye message then terminate the binary.

![image](https://github.com/user-attachments/assets/10dea23c-941e-4467-8e4b-79c40bff5c82)


9. 
