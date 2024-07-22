# Kernel Adventures: Part 1
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/77bfbef0-42b4-4a26-8ce5-e3865ff54055)


## Lessons Learned:
- Source code review.
- Exploiting race condition vuln.
- Password Hash Cracking.
- Implement double fetch exploitation.

## DESCRIPTION:
SUID binaries are too vulnerable. So I decided to implement su in the Kernel.

## STEPS:
1. In this challenge we're given the kernel environment setup.

![image](https://github.com/user-attachments/assets/65122e1a-24fb-4dbf-bcbb-fcd6d72dc17f)

![image](https://github.com/user-attachments/assets/e56eab40-ecca-4d6e-8ed1-85e50bdfdfbe)


2. Let's extract the Linux file system.

```sh
cp rootfs.cpio.gz rootfs.cpio.gz.backup
gunzip rootfs.cpio.gz
sudo cpio -i < rootfs.cpio
mv rootfs.cpio.gz.backup rootfs.cpio.gz
```

![image](https://github.com/user-attachments/assets/e5ce8c4a-9eda-420c-b413-25cc669d9fda)


3. Great! Noticed that our kernel module name is **mysu.ko**.
4. Upon decompiled the binary using ghidra, seems there are only 3 functions to interact with the module.

![image](https://github.com/user-attachments/assets/aa40a641-8260-4bdc-a451-1b6ac4be9226)


> REVIEWING dav_open()

![image](https://github.com/user-attachments/assets/fdd9ac7b-0ba2-49e3-968c-a675a13e1c73)


5. Function `dav_open()` shall not be our interest here, it just print "opened" once it's called.

> REVIEWING dav_read()

![image](https://github.com/user-attachments/assets/fca2f4df-229f-4b1c-a837-9a4c1b7ff5ef)


6. Function `dav_read()` reads up to 32 bytes of data from source **&users**, then copies it to a buffer named **param_2**.
7. If the bytes is bigger than 32, it then returns 32. Otherwise, it just returns the number of bytes copied.

> REVIEWING dav_write()

![image](https://github.com/user-attachments/assets/42a3f23c-1177-41f2-be40-eade73091c68)


8. If you noticed, `dav_write()` behavior is set to be similar to write@plt function.
9. **param2** is our content, **param3** is the size of our content, and **param1** performed as file descriptor (fd).
10. If the size of our content is less than 8, then it the binary is terminated.
11. Next, it check whether the contents of **param2** are equal to a global var named **users**.

![image](https://github.com/user-attachments/assets/625f8172-eb32-47ec-89d0-9fff39189471)


12. Afterwards, the module takes the next bytes of our input data (param2 + 1) and calc the hash. If the hash match to 0x0, then we jumped to label **LAB_0010017E**. This label uses functio `prepare_creds` and `commit_creds` to switch user. Our intention is to gained root by passing the 0 to it.
13. This is our current privilege.

![image](https://github.com/user-attachments/assets/454e9ec8-2850-439e-b314-7ecfa1689709)


14. We can further check that by running **readelf** to **mysu.ko** and check for the `.data` section.

#### NOTES:

```
Every initialized global variable that is not 0, is stored at .DATA_ADDRESS section.
```

> READELF

![image](https://github.com/user-attachments/assets/2a22de3d-3970-4f98-a8e6-e72ea29cc1e7)

![image](https://github.com/user-attachments/assets/e0013d4b-a53c-4ca9-b571-18976916e940)


15. Anyway, the vuln is at the condition where it taking again our input data from **param2**. It could introduce as **Race Condition**.
16. So when the check is passed at the beginning and we jump to label **LAB_0010017e**, we change our UID to 0 (root). Afterward the module shall perform `commit_creds(prepare_creds(0))`.
17. This type of attack in kernel exploitation is called **Double Fetch**.

### CONCERN

18. The only concern for race condition in operating system is due to the absence of **Mutual Exclusion (Mutex)** or **Binary Semaphore**.

```
[MUTEX]
- Is a locking mechanism used to ensure that only one thread
or process can access a resource at a time.

[BINARY SEMAPHORE]
- Is a signaling mechanism that can have only 2 values, 0 and 1.
It is similar to mutex but has differences in usage and behavior.
```

19. Upon reviewing at the **init_module()** function, **mutex** or **semaphore** both are absence. Hence we could gain **Race Condition** to change our UID to root.

![image](https://github.com/user-attachments/assets/c6df3ff9-5874-4789-b50d-f23fa3140547)


20. Great! Seems we found the bug now.
21. First, let's get the expected hash to find a valid password. Execute `run.sh` file to start the kernel emulation.
22. To get the expected hash, run `dd` from `/dev/mysu` to extract the users variable we saw before.

> RESULT

```
dd if=/dev/mysu count=4 | xxd
```

![image](https://github.com/user-attachments/assets/01697716-08dc-45dc-acaa-6bf0afd4f6e0)


23. Well, if you remembered the notes.txt file at the beginning. It states that the password hashes is removed. But it should not be 0.
24. Let's check at the remote server.

> REMOTE SERVER

![image](https://github.com/user-attachments/assets/caca02a1-9790-4089-b832-a3eb04cf3ce8)


25. So the expected hash in hex format is `0x03319f75`.
26. To obtain this hash, we have to use the same hashing function found in the **mysu.ko**.

> The hashing function

![image](https://github.com/user-attachments/assets/708522f9-f7a7-451b-ac19-bcfbd66a8484)


27. Since the valid password length is 8 bytes, meaning **2 to the power of 68** and very time consuming because the only way to get the valid pass is by bruteforcing it.
28. To speed up the process, we can use **angr** or **z3** library in python. But in this writeup I will show the result for using both. Also we need to compile the C hash function so we can validate whether our password is correct.

> SCRIPT TO BRUTEFORCE --> using Z3

```py
from pwn import *
import os
from z3 import *

result = 0
target_hash = 0x03319f75
byte_array = [BitVec(f'byte index {i}', 8) for i in range(8)]

for byte in byte_array:
    extended_byte = SignExt(24, byte)
    intermediate_res = (result + extended_byte) * 0x401 # 1025
    result = intermediate_res ^ LShR(intermediate_res, 6) ^ extended_byte

# Create a Z3 solver instance
solver = Solver()

# Constraint to solver, that the calc hash must equal to targ hash.
solver.add(result == target_hash)

# if constraint is satisfiable
if solver.check() == sat:
    model = solver.model()
    log.success(f'Correct hash found')
    # print result
    print(bytes(model[byte].as_long() for byte in byte_array))
```

#### NOTES:

```
1. Using SignExt because char type in C is signed.
2. Using LShR to perform logical bit-shift.
```

> THE C SOURCE

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

unsigned int hash(char *string) {
  int i;
  unsigned int uvar1;
  unsigned int res;

  res = 0;

  for (i = 0; i < strlen(string); i++) {  
    uvar1 = (res + string[i]) * 0x401;
    res = uvar1 ^ uvar1 >> 6 ^ string[i];
  }

  return res;
}

int main() {
  char password[8];
  scanf("%s", password);
  getchar();

  if (hash(password) == 0x03319f75) {
    puts("Yes");
  } else {
    puts("Nope");
  }

  return 0;
}
```

> RESULT

![image](https://github.com/user-attachments/assets/ac41eaf8-428e-4978-af64-1dfa28469e0a)

> WITH ANGR

```py
from pwn import *
import os 
import angr

exe = angr.Project('./hash-bin')

# create the initial state of the program (at the entry point)
init_state = exe.factory.entry_state()

# create a simulation manager to manage the exploration of states
sim_manager = exe.factory.simulation_manager(init_state)

# explore the state space to find a state where "Yes" is printed to fd 1 (stdout)
sim_manager.explore(find=lambda state: b'Yes\n' in state.posix.dumps(1))

if sim_manager.found:
    found_state = sim_manager.found[0]
    pass_bytes = found_state.posix.dumps(0) # extract input

    # conver the input bytes to a list of hex strings
    pass_hex = (hex(byte) for byte in pass_bytes)
    print(', '.join(pass_hex))
```

> RESULT WITH ANGR

![image](https://github.com/user-attachments/assets/0cbeceaf-d378-4b83-b650-f5414d0467b6)


29. Nice! Now let's craft our exploit.
30. Remembering we're going to abuse a **Double Fetch**, hence using 2 threads shall required to win the race.
31. One thread is used to continuously changing our UID to 0 in our input data.
32. The other one is used to continuously changing our UID to 1000 in our input data.
33. There should be a moment where, the module checks our UID (at this rate is 1000), then we passed. Afterwards our UID changed to 0 before the module fetch the user input data again to call `commit_creds(prepare_creds())`.
34. Finally. once our UID is changed to 0, we stop all running threads.

> EXPLOIT C CODE

```c

```

## FLAG

```
HTB{C0ngr4ts_y0u_3xpl0it3d_A_D0uBlE-FeTcH}
```
