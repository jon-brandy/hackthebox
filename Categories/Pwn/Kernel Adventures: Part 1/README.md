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
4. Let's decompiled it using ghidra to review the code.

## FLAG

```
HTB{C0ngr4ts_y0u_3xpl0it3d_A_D0uBlE-FeTcH}
```
