# r0bob1rd
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/bfbb32ec-47d7-49f2-b7f6-87a5e801f3a5)


## Lessons Learned:
1. Leak LIBC by clobbering with array index.
2. Utilize FSB to perform GOT overwrite for `__stack_chk_fail()` function.
3. Using `Out-of-Bound (OOB)` bug to trigger `__stack_chk_fail()` function call.

## DESCRIPTION:

<p align="justify">I am developing a brand new game with robotic birds. Would you like to test my progress so far?</p>

## STEPS:

1. In this challenge we're given a 64-bit binary, dynamically linked, not stripped.

![image](https://github.com/user-attachments/assets/8252e70c-0f1d-46e0-8ee0-2689917d3216)

> BINARY PROTECTIONS

![image](https://github.com/user-attachments/assets/e120d82d-1c0e-4764-a3b9-da22510c16d3)

> REVIEWING THE CODE

2. Upon reviewing the code at Ghidra, found few bugs reside at the **operation()** function.

![image](https://github.com/user-attachments/assets/e7b166eb-9c58-4ebc-9090-6cbd8588e519)


3. It's very straight forward, there is a chance for us to leak libc address at the first user input (number). Because what printed to us is the value stored at the index array of initialized global variable **robobirdNames**.
4. Notice that there is no proper bound checking for our input, so if we input negative values, we could print adjacent memory address.

![image](https://github.com/user-attachments/assets/d4078e0d-16e0-4d52-a62a-b6657306453b)

5. Anyway, since it is initialized global variable, hence we can review all the entry contents address from the `.data` section.

> .DATA SECTION


![image](https://github.com/user-attachments/assets/e7b62d7d-ce07-4530-bcef-54d271a13e98)


