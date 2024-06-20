# Sound of Silence

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c00cb1d6-aa6b-4bff-b60d-65115285d01f)


> Write-up author: jon-brandy

## Lessons Learned:
1. Stack-Based Exploitation.
2. Manipulate return address to gets(), then use system() as it's argument.

## DESCRIPTION:

<p align="justify">Navigate the shadows in a dimly lit room, silently evading detection as you strategize to outsmart your foes. Employ clever distractions to divert their attention, paving the way for your daring escape!</p>

## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5e40093d-ac65-4955-9bb6-93899c3d2a2f)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e53e26ae-0d6c-457f-a5d7-e643dec8c82e)


2. This time the soure code is disclosed. Upon reviewing the source, it's very clear the vuln is at the **gets()** usage.
