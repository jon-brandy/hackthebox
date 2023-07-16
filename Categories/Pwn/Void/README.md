# Void
> Write-up author: jon-brandy
## DESCRIPTION:
The room goes dark and all you can see is a damaged terminal. Hack into it to restore the power and find your way out.
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary - not stripped.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/051edd67-8036-4c74-bdbc-9f7a144140ec)

> No Canary Found, PARTIAL RELRO, NO PIE

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/883735c5-0bb9-4f85-9485-e5de52f1ce4e)


2. Let's decompile the binary with ghidra.
3. At the main() function, there's only one function called --> vuln()

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/c762cb32-c0fd-4976-b2af-6725b8c9965b)


4. At first, i assume that the chall must be related to `ret2libc` because there's no interesting function to return to.
5. But after checking the **Global Offset Table** turns out there are no `puts()`, `printf()`, or `write()` functions.
6. Then i realized it's a `ret2dlresolve` pwn challenge. It's a technique in pwn to manipulate the dyanmic linker's resolution process and redirect it to execute arbitrary code.
7. Actually it's `quite similiar` to overwrite GOT with format strings vuln.
8. Also we can utilize **pwntools** to automate the process to resolve the functions, because if we don't use pwntools, we need to construct.
