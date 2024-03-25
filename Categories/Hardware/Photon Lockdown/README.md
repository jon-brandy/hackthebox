# Photon Lockdown
> Write-up author: jon-brandy

## Lessons Learned:
- Extracting a squash file using unsquashfs.

## HINT:
- NONE

## DESCRIPTION:
We've located the adversary's location and must now secure access to their Optical Network Terminal to disable their internet connection. 
Fortunately, we've obtained a copy of the device's firmware, which is suspected to contain hardcoded credentials. Can you extract the password from it?

## STEPS:
1. In this challenge we're given 3 files. `fwu_ver` and `hw_ver` seems not our interest (judging from the filesize).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e1b32183-da4c-4ae1-bcb5-a97a43acd248)


2. Noticed there's a **rootfs** file, it's a squash file which means a compressed read-only filesystem format commonly used in Linux distributions and embedded systems. It allows for efficient storage and distribution of file systems by compressing them into a single file.
3. To unsquash it we can use --> `sudo unsquashfs rootfs`.

> CONTENT OF ROOTFS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0fe0db4c-f2cf-4182-a463-5f7e82c70140)


4. Seems our objective is to find the flag locations. Actually I found 2 methods, the first one is the method used for linux privesc to identify custom binaries, password stored, or else.

```
COMMAND:

grep --include=*.{txt,xml,php,py,conf,yml} -rnw '.' -ie 'HTB' 2>/dev/null
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a700112a-61fe-465d-837f-19435761a109)


5. The second method is just strings all the available files inside the directories and grab for the flag's prefix.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a375bbaa-938b-41ec-8dee-f4928d59d0e7)


6. Anyway, we got the flag!

## FLAG

```
HTB{N0w_Y0u_C4n_L0g1n}
```
