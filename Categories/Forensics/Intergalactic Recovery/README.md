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
9. Now let's use **losetup** to setup and control loop devices.

```
sudo losetup /dev/loop1 fef0d1cd.img
sudo losetup /dev/loop2 06f98d35.img
sudo losetup /dev/loop3 disk3.img
```

![image](https://user-images.githubusercontent.com/70703371/211968964-bb8e4210-bae9-464b-8846-ecfc35d78f62.png)

 
10. Next, let's use **mdadm**, it's used for 


