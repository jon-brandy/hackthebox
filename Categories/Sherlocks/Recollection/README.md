# Recollection
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c18c9fa8-036f-4af8-935b-71b53fa33dc9)


## Lessons Learned:
- Using volatility to do RAM forensic.
- Identifying an alias usage for IEX.

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

> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8685233d-1834-4426-98a0-9cb2afe2ea39)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/da73e2fb-557c-4841-ac27-0ec8df50bb3b)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8962f6b2-47b0-43fe-bf87-37389cf8afde)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/82aedfbf-4d94-47f0-807f-a5c71fd1f00f)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/216d4aa9-c65b-49fa-b982-729707aace9c)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a267ab2c-6c2a-48f4-955c-ee4483942076)


> 11TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/17f08389-3aae-44c1-afbc-246b0962e5eb)


> 12TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/806b20de-cdf6-477a-9ed0-aa8441aaa570)


> 13TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b643844b-32b7-41be-ba93-66a07d9e45af)


> 14TH QUESTIOM --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/efa3420a-8ad4-4376-bb99-c1ead9eae52d)


> 15TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ae56ce46-fa25-4c54-bfa4-61c206980d2b)


> 16TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/316f936d-35d7-4643-a960-c626e0f28a6a)


> 17TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9a9c3b94-43a7-44a1-b7f9-5eb8cac0d83d)


> 18TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b8400da6-5b77-4217-98d7-4b90de761802)


## IMPORTANT LINKS

```
https://www.securonix.com/blog/hiding-the-powershell-execution-flow/
```
