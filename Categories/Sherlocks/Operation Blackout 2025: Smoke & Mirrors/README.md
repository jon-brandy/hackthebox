# Operation Blackout 2025: Smoke & Mirrors
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/1dfc6074-a86f-47e1-9292-5c7b59c88e90)


## Lessons Learned:
1. Utilized Hayabusa to parse Windows event logs into CSV format, with severity tags highlighting notable events.
2. Employed Timeline Explorer to efficiently examine and filter through the CSV timeline data.
3. Identified indicators of attempts to disable Windows Defender and LSA (Local Security Authority) protection.
4. Detected an AMSI (Antimalware Scan Interface) patch attempt, commonly used to bypass in-memory script scanning.
5. Observed activities aimed at restarting the system in Safe Mode and disabling PowerShell command history logging, indicating efforts to evade detection and maintain stealth.

## SCENARIO:

<p align="justify">Byte Doctor Reyes is investigating a stealthy post-breach attack where several expected security logs and Windows Defender alerts appear to be missing. He suspects the attacker employed defense evasion techniques to disable or manipulate security controls, significantly complicating detection efforts. Using the exported event logs, your objective is to uncover how the attacker compromised the system's defenses to remain undetected.</p>

## STEPS:
1. In this case, we were tasked with investigating a scoped and niche activity. Preliminary observations indicated that several security logs and Windows Defender alerts were missing, suggesting that the threat actor may have employed defense evasion techniques to disable or manipulate security controls.
2. Our objective was to verify whether such activities were actually conducted and, if confirmed, to provide concrete evidence of the threat actor’s actions.
3. Since our objective is very straightforward, we can speed up the investigation using a tool to parse event logfiles to a CSV file containing severity tags highlighting notable events.
4. This time I used Hayabusa which is a tool developed by Yamato Security.

> COMMAND:

```
hayabusa-3.3.0-win-x64.exe csv-timeline -d C:\HTB-SHERLOCKS\ -o results.csv -p super-verbose
```

5. Using the command above, my objective was to parse all event logs located in the HTB-SHERLOCKS directory, which contained the forensic evidence. I utilized the --csv-timeline flag to instruct Hayabusa to convert the parsed data into a CSV timeline format, and the -o flag to specify the output file name as results.csv.
6. Additionally, I enabled the --super-verbose flag to ensure Hayabusa provided detailed output regarding its scanning findings, which helped in identifying relevant artifacts more efficiently.

> I CHOOSE THE 3RD OPTION SCAN RULE AND ENABLE SYSMON SCAN

![gambar](https://github.com/user-attachments/assets/7f25305c-89d1-45ed-b333-e5cdff7b3283)

![gambar](https://github.com/user-attachments/assets/c4d727ee-623f-4e47-994f-199fb175ffd8)

7. Great! It seems Hayabusa indeed captures all activities related to our interest.

![gambar](https://github.com/user-attachments/assets/87d9c962-4fe9-49a3-97a3-067d5d3a0da1)


> 1ST QUESTION -> ANS: `HKLM\SYSTEM\CurrentControlSet\Control\LSA`

![image](https://github.com/user-attachments/assets/fdd0431d-5d3b-4d8c-b086-7c7bd4c0838d)

8. I reviewed the CSV output file using Timeline Explorer, a forensic analysis tool developed by Eric Zimmerman.
9. Searching for LSA resulting to an interesting event at `2025-04-10 13:28:47`.
10. An attempt to disable LSA PPL Protection via reg.exe binary.

![gambar](https://github.com/user-attachments/assets/cfcfdacc-b33a-4370-8b88-d4f3e3d3654e)

11. Reviewing the command line, its clear that the threat actor abusing LSA registry key -> `HKLM\SYSTEM\CurrentControlSet\Control\LSA`.

![gambar](https://github.com/user-attachments/assets/66116468-fb6f-40c9-bea4-99c84be49a74)


> 2ND QUESTION -> ANS: `Set-MpPreference -DisableIOAVProtection $true -DisableEmailScanning $true -DisableBlockAtFirstSeen $true`

![image](https://github.com/user-attachments/assets/2938d0df-8662-4d05-acb2-8bffc9776c1e)

12. To identify activity related to Windows Defender, usually I used 2 search keywords in Timeline Explorer -> `Mp` and `Set-MpPreference`.

> RESULT

![gambar](https://github.com/user-attachments/assets/b1884b98-dbea-4dab-8215-d006e9e375f7)


13. Between the timestamps `2025-04-10 13:31:32` and `2025-04-10 13:37:05`, identified three HIGH-severity events related to Windows Defender tampering.

![gambar](https://github.com/user-attachments/assets/0c95453e-f622-4e7a-b4df-e7af34bc7269)

14. Based from it, its clear that the first command executed is:

```pwsh
Set-MpPreference -DisableIOAVProtection $true -DisableEmailScanning $true -DisableBlockAtFirstSeen $true
```

#### NOTES:

```MD
Set-MpPreference -> PowerShell cmdlet for configuring Windows Defender preferences.
-DisableIOAVProtection $true -> Disables real-time file scanning (Input/Output Anti-Virus).
-DisableEmailScanning $true -> Disables email attachment scanning.
-DisableBlockAtFirstSeen $true -> Disables cloud-based protection for unknown files.
```

![gambar](https://github.com/user-attachments/assets/d3bba171-f640-4a74-ab60-9b83b4a65d2a)


> 3RD QUESTION -> ANS: `AmsiScanBuffer`

![image](https://github.com/user-attachments/assets/42116564-9af8-45ed-9af9-5d8ae58597e7)

15. Afterward, the threat actor appeared to attempt invoking Windows API (WinAPI) functions through PowerShell scripts, likely to perform low-level operations while evading traditional detection methods.

![gambar](https://github.com/user-attachments/assets/bc33201b-b76f-423d-a009-88f662109265)

![gambar](https://github.com/user-attachments/assets/b41be274-eefd-4960-9e7c-fd4e525afaaa)

16. The script above should be our interest and likely it is used to implements an AMSI (Antimalware Scan interface) bypass technique. 

![gambar](https://github.com/user-attachments/assets/fd9d8e28-ea58-4f2b-a421-94000aebe0af)


17. We observed that the AMSI function name AmsiScanBuffer() was obfuscated and assigned to a variable named a. Following this, a memory patch was applied to the function’s address using inline assembly instructions, indicating an attempt to bypass AMSI scanning.

![gambar](https://github.com/user-attachments/assets/6b4e05c3-7009-43e6-a66a-e8a29a97851b)


> 4TH QUESTION -> ANS: `bcdedit.exe /set safeboot network`

![image](https://github.com/user-attachments/assets/db84d7fa-cd17-4055-98ae-1995c02b6f36)

18. Shortly after, at timestamp `2025-04-10 13:38:35`, an attempt to tamper with the Master Boot Record (MBR) was identified through the use of bcdedit.exe, suggesting efforts to modify boot configuration settings—potentially to enable persistence or boot into Safe Mode.
19. Reviewing the details, found the exection performed is to modifies the system boot settings.
20. It configures the system to boot into safe mode with networking.

```
"C:\WINDOWS\system32\bcdedit.exe" /set safeboot network
```

![gambar](https://github.com/user-attachments/assets/74292dfe-13d9-4ec2-9e5b-10560edce14e)


> 5TH QUESTION -> ANS: `Set-PSReadlineOption -HistorySaveStyle SaveNothing`

![image](https://github.com/user-attachments/assets/92ca9265-774e-474a-835e-371d3f7da9a8)


21. Continue reviewing the threat actor's activity, at timestamp `2025-04-10 13:38:43` found an attempt to disable powershell command history logging.

![gambar](https://github.com/user-attachments/assets/bf7bb0b6-4885-48cd-973d-06bb1ab59f24)

![gambar](https://github.com/user-attachments/assets/82753a68-f7c1-4815-a11e-f68a3708b412)

> COMMAND:

```
Set-PSReadlineOption -HistorySaveStyle SaveNothing
```

22. Great! We've investigated a quick case and specific request!

## IMPORTANT LINKS:

```
https://github.com/Yamato-Security/hayabusa
```
