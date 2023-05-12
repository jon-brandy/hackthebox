# Extraterrestrial Persistence
> Write-up author: vreshco
## DESCRIPTION:
There is a rumor that aliens have developed a persistence mechanism that is impossible to detect. 
After investigating her recently compromised Linux server, Pandora found a possible sample of this mechanism. 
Can you analyze it and find out how they install their persistence?
## HINT:
- NONE
## STEPS:
1. Unzipping the file shall resulting a bashscript file.

> THE SCRIPT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/8393ef56-60e7-4f95-85d2-bd2fb552346b)


2. Notice there's a base64 and the decoded value stored to `/usr/lib/systemd/system/service.service`. Let's grab the base64 text and decode it.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/cb722eed-236f-4f15-92da-b29e99a9745a)


3. Got the flag!

## FLAG

```
HTB{th3s3_4l13nS_4r3_s00000_b4s1c}
```
