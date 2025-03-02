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


![image](https://github.com/user-attachments/assets/2e198915-7642-4e8b-9451-38d6f2eb0b5e)


6. Notice that the **.data** section is close to **.got** section memory. So we could actually leak the libc function by passing the correct index number. Now to identify it, let's examine the mapped GOT dynamically using **GDB**.

> IN GDB


![image](https://github.com/user-attachments/assets/042d12c3-f14d-4aec-b3de-035a735ab6ec)


7. Actually to leak libc we can't use any of them, we need to choose the GOT address that if we add to the formula of the printed address, the result should be pointing to GOT address.

```MD
> FORMULA:
nobobirdNames + (input * 8) = MUST_BE_GOT_ADDRESS
```

> AVAILABLE GOT FUNCTIONS TO BE USED (INSIDE THE RED BOX)


![image](https://github.com/user-attachments/assets/4c97b94a-6869-4d26-8ccf-7712287659f1)


8. In this case, there are several GOT address can be used and in this writeup I choose the **setvbuf@got**.

![image](https://github.com/user-attachments/assets/f6f1dc49-da51-4c03-8c3b-58c7613bbf74)


9. Great! Now we need to pass **-0x8** and parse the libc leak.
10. Next, the rest is also straightforward, we just need to identify the offset for our FSB write and it seems our only GOT function overwrite candidate should be the **_stack_chk_fail()**, because that is the only function called after the FSB.


![image](https://github.com/user-attachments/assets/705cea94-48ff-4631-b228-5a22bfa6a845)


11. Great! Next, upon reviewing the correct **one_gadget** that would be used, found the candidate is the second one. As you can see below, the **R15** does pointed to null and **RDX** is not -> 0x1. However another OR condition, state that if **RDX** is an envp hence we can use it.
12. To verify it we can simply break at main then query -> `x/s *(char **) $rdx`.

#### NOTE:

```MD

# According to system V calling convention:
RDI → argc
RSI → argv
RDX → envp

int main(int argc, char *argv[], char *envp[]);
```

> RESULT

![image](https://github.com/user-attachments/assets/77a81f18-5c5d-402a-8f41-2c973ac96929)


![image](https://github.com/user-attachments/assets/0547ce86-fe38-40b0-b847-7d2e0d00a11b)


13. Awesome! Everything is going smooth.
