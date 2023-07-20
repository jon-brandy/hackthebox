# Fleet Management
> Write-up author: jon-brandy
## DESCRIPTION:
Reading through an Underground Intergalactic hacking forum Bonnie stumbles upon a post talking about a backdoor in the Gold Fang’s Spaceship Fleet Management System. 
There is a note about a twist added by the author to prevent anyone from using the backdoor. 
Will Bonnie achieve to gain access to Gold Fang’s internal network and retrieve precious documents?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/01e498a8-ad99-4299-8d88-13f78a1cc1d6)


> BINARY PROTECTIONS

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/2de5a421-f79f-4f92-ae29-8249a21a1476)


2. After decompiled the binary, it looks like there's a hidden menu which calls the **beta_feature()** function.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/1ead0cbe-4f84-4235-ad05-5931745906c3)


3. There's a chance we can do shellcode injection even though the NX are disabled.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/c624695a-1467-4a47-88fd-cc9bf0dcaa64)


4. But the problem is, we have `seccomp()`. (`skid_check()`)
