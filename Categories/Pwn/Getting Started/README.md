# Getting Started
> Write-up author: vreshco
## DESCRIPTION:
Get ready for the last guided challenge and your first real exploit. It's time to show your hacking skills.
## HINT:
- NONE
## STEPS:
1. Given 3 files, the glibc directory, 64 bit binary file, fake flag, and a snippet script for sending the payload.
2. Check the binary's protections.

> VULN -> No Canary Found.

![image](https://user-images.githubusercontent.com/70703371/233819245-9bed099d-b41d-440e-9320-656fd4364bd5.png)


3. Let's decompile the binary.

![image](https://user-images.githubusercontent.com/70703371/233819303-35ad69db-4dd5-4b4d-b6a6-53ceeb261daa.png)


4. Found the bufferoverflow there, which we can use to modify the value stored at `local_10`.
5. No need to find the RIP offset, but if you want to it's at 56 bytes.

![image](https://user-images.githubusercontent.com/70703371/233819411-0be785b7-6117-411c-be66-b1837a304e90.png)


6. We can get the flag by sending bytes > 56, because the next bytes shall overwrite the value stored at `local_10` to other than 0xdeadbeef.
7. Let's test it locally.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/233819435-1687941c-cd1d-4f4b-9573-de211c8e52c0.png)


> REMOTELY

![image](https://user-images.githubusercontent.com/70703371/233819517-166f08d8-6e76-4046-ba15-40227572b831.png)


8. Got the flag!

## FLAG

```
HTB{b0f_tut0r14l5_4r3_g00d}
```
