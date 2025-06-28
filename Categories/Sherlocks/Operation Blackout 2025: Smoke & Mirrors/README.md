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


> 1ST QUESTION -> ANS:

![image](https://github.com/user-attachments/assets/fdd0431d-5d3b-4d8c-b086-7c7bd4c0838d)

8. I reviewed the CSV output file using Timeline Explorer, a forensic analysis tool developed by Eric Zimmerman.
9. Searching for LSA resulting to an interesting event at `2025-04-10 13:28:47`.
10. An attempt to disable LSA PPL Protection via reg.exe binary.

![gambar](https://github.com/user-attachments/assets/cfcfdacc-b33a-4370-8b88-d4f3e3d3654e)

11. Reviewing the command line, its clear that the threat actor abusing LSA registry key -> `HKLM\SYSTEM\CurrentControlSet\Control\LSA`.

![gambar](https://github.com/user-attachments/assets/66116468-fb6f-40c9-bea4-99c84be49a74)


> 2ND QUESTION -> ANS:

![image](https://github.com/user-attachments/assets/2938d0df-8662-4d05-acb2-8bffc9776c1e)


> 3RD QUESTION -> ANS:

![image](https://github.com/user-attachments/assets/42116564-9af8-45ed-9af9-5d8ae58597e7)


> 4TH QUESTION -> ANS:

![image](https://github.com/user-attachments/assets/db84d7fa-cd17-4055-98ae-1995c02b6f36)


> 5TH QUESTION -> ANS:

![image](https://github.com/user-attachments/assets/92ca9265-774e-474a-835e-371d3f7da9a8)


## IMPORTANT LINKS:

```
```
