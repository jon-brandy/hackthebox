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


2. Let's extract the Linux file system.

```
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

![image](https://github.com/user-attachments/assets/e3e5c02b-7007-4e10-97ad-81252c141f4f)


8. If you noticed, `dav_write()` behavior is set to be similiar to write@plt function.
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



## FLAG

```
HTB{C0ngr4ts_y0u_3xpl0it3d_A_D0uBlE-FeTcH}
```
