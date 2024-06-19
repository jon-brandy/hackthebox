# Rocket Blaster XXX
> Write-up author: jon-brandy

## Lessons Learned:
1. ROP gadgets.
2. Manipulate return address.
3. Popping 3 gadgets.

## DESCRIPTION:

<p align="justify">Prepare for the ultimate showdown! Load your weapons, gear up for battle, and dive into the epic fray—let the fight commence!</p>

## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2cdc17fb-5d88-45ec-8a5e-7064831289ec)

> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b1dcc35f-4b1c-4a7d-8c56-d1ebb6adf6d9)

2. Upon reviewing the decompiled code on ghidra, we can see the main() function only accepts 1 input then terminate the process.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5f536ba1-7a27-4e01-8a2e-948f1ff74397)


3. Reviewing other functions, we noticed a function named `fill_ammo` which opens the flag but not stored directly onto the stack.



## FLAG

```
HTB{b00m_b00m_b00m_3_r0ck3t5_t0_th3_m00n}
```
