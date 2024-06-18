# Execute
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a76f9eac-e18c-4903-866d-87de83421845)


## Lessons Learned:
1. Stack-Based Exploitation.
2. Input bug which leads to direct code execution.
3. Implement ret2shellcode attack.
4. Craft custom shellcode to bypass bad bytes.

## DESCRIPTION:

## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f25e6b28-c6a8-437f-9eeb-a910233a9085)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2419960c-7a0c-408f-b15a-22e30567fc39)


2. Interesting! NX is disabled here. Hence it should be easier for us to gain RCE.
3. Upon reviewing the source code, our objective is very straightforward.
4. There is no buffer overflow, we just need to send our shellcode and it shall executed onto the stack.
5. BUT, the problem is there are several filters to our shellcode, which require us to craft our own shellcode.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/30e29a82-0d47-489d-82ab-a37bc286363b)

6. The easiest way to check which bytes is filtered, simply craft basic shellcode then compare which byte match the pattern.

> SCRIPT

```py

```
