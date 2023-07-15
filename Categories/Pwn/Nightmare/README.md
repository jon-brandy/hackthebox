# Nightmare
> Write-up author: jon-brandy
## DESCRIPTION:
You seem to be stuck in an endless nightmare. Can you find a way out?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary , stripped, and with **NO RELRO**.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/05cea160-e903-4d4d-a710-7caac4a7acad)

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4ba73284-daca-4972-98d7-029cc3d7751c)


2. The exploit here is we need to leak the leak and calculate the piebase and libc_base then.
3. After decompiled the binary using ghidra, i noticed there's a format string vulnerability for first option menu and second option menu.

> This function called when user choose the 1st option menu.

#### NOTES: The format string vuln found at line 12, the binary seems not specify the output format.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/8e3b5d39-54d2-4899-b8d8-1628b7c5e2ec)


> This function called when user choose the 2nd option menu.

#### NOTES: The format strings vuln found at line 19.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4034274f-e571-4ff5-b207-26f3010dbd35)

