# Intergalactic Recovery
> Write-up author: jon-brandy
## DESCRIPTION:
Miyuki's team stores all the evidence from important cases in a shared RAID 5 disk. 
Especially now that the case IMW-1337 is almost completed, evidences and clues are needed more than ever. 
Unfortunately for the team, an electromagnetic pulse caused by Draeger's EMP cannon has partially destroyed the disk. 
Can you help her and the rest of team recover the content of the failed disk?
## HINT:
- NONE
## STEPS:
1. First, unzipt the `.zip` file given, then jump to the extracted directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/211962972-b930eee3-5811-461f-8a2a-9c7859bc0036.png)


![image](https://user-images.githubusercontent.com/70703371/211963263-84b97460-4b27-4a23-906c-4d10a677688f.png)


![image](https://user-images.githubusercontent.com/70703371/211963318-c927eb21-0b3b-4ece-b663-ffa043f45c88.png)


2. When tried to see the disk size, we know that `0c584923.img` might be corrupted because the size is so small.
3. Based on the description, this chall shall related to **RAID 5**. 
4. Well i won't explain about **RAID 5**, you can read the documentation about it here:

```
https://www.techtarget.com/searchstorage/definition/RAID-5-redundant-array-of-independent-disks
https://www.forensicfocus.com/articles/making-complex-issues-simple-a-unique-method-to-extract-evidence-from-raid-with-lost-configuration/
```

5. First, we need to XOR the file with same sizes so we can get the recovered disk, to do this i use pwntools.

> THE SCRIPT

```py
from pwn import *
import os

os.system('clear')

disk1 = read('fef0d1cd.img')
disk2 = read('06f98d35.img')
disk3 = xor(disk1, disk2)

write('disk3.img', disk3) # save the recovered disk
```

6. After run the script, strings the `disk3.img` to see if we can get any clue.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211967588-f12fc925-d0e2-408c-9cc7-7e79f61164f2.png)


7. Seems like there's a pdf file inside it, let's run **foremost**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211967878-b81b4602-853a-4e92-96cc-77c68c3204f6.png)


![image](https://user-images.githubusercontent.com/70703371/211967969-3f860565-9f5d-42e0-9777-37c1ba5578c2.png)


8. Yep it's obviously still corrupted, because we still need to reconfigure the raid 5.
9. Now before going any further, i already done it to the end and still can't open the pdf file. So i did a small outsource about this problem and found out that we need to switch the disk2 and disk3. What i intend to say is, we need to change the order of the disk. So the disk2 shall renamed to disk3, and disk3 shall renamed to disk2


![image](https://user-images.githubusercontent.com/70703371/211974289-47bd2c89-84b3-4553-85a7-141e2ba6719c.png)


9. Now let's use **losetup** to setup and control loop devices.

```
sudo losetup /dev/loop1 disk1.img
sudo losetup /dev/loop2 disk2.img
sudo losetup /dev/loop3 disk3.img
```

![image](https://user-images.githubusercontent.com/70703371/211968964-bb8e4210-bae9-464b-8846-ecfc35d78f62.png)

 
10. Next, let's use **mdadm**, it's used for manage MD devices aka Linux Software RAID

```
sudo mdadm --create --level=5 --raid-devices=3 /dev/md0 /dev/loop1 /dev/loop2 /dev/loop3
```

![image](https://user-images.githubusercontent.com/70703371/211970653-51c0780a-de42-495d-8940-4b7904108020.png)


> FOLLOW THIS STEP TO MOUNT THE DISK

![image](https://user-images.githubusercontent.com/70703371/211970744-cb49acf3-590a-47ae-b586-772c2de770b2.png)

```
sudo mount /dev/md0 /mnt/raid
```

![image](https://user-images.githubusercontent.com/70703371/211970973-944f2f0e-8f12-4e57-a5fe-21d8e0ac501a.png)


11. Check what we get inside.

![image](https://user-images.githubusercontent.com/70703371/211971117-3c58568d-1927-49a1-91aa-f940d8d565a3.png)


12. Let's copy that to our current directory, then open the pdf file.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/211978216-a3709706-6190-41b9-9389-cb7ab75f616a.png)


13. Got the flg!

## FLAG

```
HTB{f33ls_g00d_t0_b3_1nterg4l4ct1c_m0st_w4nt3d}
```
