# SmartyPants
> Write-up author: jon-brandy

![image](https://github.com/user-attachments/assets/6e7472c6-bf29-469d-92bb-49e8b948fd46)


## Lessons Learned:
1. Identify & Analyze Windows RDP-Related Event Logs.
2. Using **event log explorer** and **event viewer** to analyze windows event logs.
3. Reviewing **Smart Screen Debug** logs.

## SCENARIO:

<p align="justify">Forela's CTO, Dutch, stores important files on a separate Windows system because the domain environment at Forela is frequently breached due to its exposure across various industries. On 24 January 2025, our worst fears were realised when an intruder accessed the fileserver, installed utilities to aid their actions, stole critical files, and then deleted them, rendering them unrecoverable. The team was immediately informed of the extortion attempt by the intruders, who are now demanding money. While our legal team addresses the situation, we must quickly perform triage to assess the incident's extent. Note from the manager: We enabled SmartScreen Debug Logs across all our machines for enhanced visibility a few days ago, following a security research recommendation. These logs can provide quick insights, so ensure they are utilised.</p>

## STEPS:
1. On 24 January 2025, an intruder gained unauthorized access to Forela’s fileserver, installed utilities to facilitate their actions, exfiltrated critical files, and then deleted them to prevent recovery.
2. This security breach has led to an extortion attempt, with the attackers demanding a ransom. The legal team is currently handling the extortion aspect, but our primary focus is conducting an immediate triage to assess the full extent of the incident.

> 1ST QUESTION -> ANS: `2025-01-24 10:15:14`

![image](https://github.com/user-attachments/assets/d94bdf93-6369-4e65-bb2f-fc1fc3ea9d17)

3. To review the log for logon using RDP, there are many RDP-related event logs. Interestingly, the logon attempt is not logged inside the Security event log. As you can see below, there is no successful logon with logon type 10.

![image](https://github.com/user-attachments/assets/8dec4e05-b8f3-4dad-86f9-e912e6076013)


4. Note that there are many event logs related to RDP and in this case we could identify the logon attempt from this event log -> `Microsoft-Windows-TerminalServices-RemoteConnectionManager%4Operational.evtx`.
5. Upon reviewing the log, found the log that indicates successful event logon at timestamp `2025-01-24 10:15:14` and reviewing other logs, no other RDP login attempt.
6. This should be the initial login access of the attacker, because there is no other login attempt.

![image](https://github.com/user-attachments/assets/64bf5f50-f493-4f09-a4e1-76611ec54cfa)


> 2ND QUESTION -> ANS: `WinRAR`

![image](https://github.com/user-attachments/assets/50b412a0-82a6-4f18-954f-d61ded782e47)

7. We can further investigate the threat actor's activity with ease, because the **Smart Screen Debug Logs** is enabled.
8. Note that, **Smart Screen Debug Logs** is from **Microsoft Defender SmartScreen** and this function primarily works as preventive measure rather than tool / binary removal. Which means it focuses on protecting users from malicious downloads, websites, and app installers.
9. So if we found the C2 or malicious binary installation performed by the threat actor, it shall shown at the log.
10. Upon reviewing the log, not long after the initial access, at `2025-01-24 10:17:14` a **WinRAR** software setup binary is executed.

![image](https://github.com/user-attachments/assets/d94533d6-24e9-4cb4-8647-37dd0ec812a1)

> WinRAR.exe binary execution

![image](https://github.com/user-attachments/assets/a6eaec8e-abe3-4f01-bea0-3635b7746553)


> 3RD QUESTION -> ANS: `C:\Users\Dutch\Downloads\Everything.exe`

![image](https://github.com/user-attachments/assets/cd70cd64-c2d5-4178-939b-e9db77473350)

11. Next, continue reviewing the log, we can identify another interesting binary named **Everything.exe** executed at timestamp `2025-01-24 10:17:33`.
12. Searching on the internet regarding this binary, found a research article published by **CYRFIRMA** regarding **ELPACO-team Ransomware**.

![image](https://github.com/user-attachments/assets/a7d57f46-43ed-4a8f-8799-fa698bb18a51)

13. The binary seems a file search utility.

> 4TH QUESTION -> ANS: `2025-01-24 10:17:33`

![image](https://github.com/user-attachments/assets/6b3be03d-d7c0-4883-9ca9-5cc49bfc4fad)


14. Based on our previous finding, the execution timestamp is `2025-01-24 10:17:33`.


> 5TH QUESTION -> ANS: `C:\Users\Dutch\Documents\2025- Board of directors Documents\Ministry Of Defense Audit.pdf`

![image](https://github.com/user-attachments/assets/94d2b3ef-8add-4d7e-a267-1ba5670d2263)


15. Next, upon continue reviewing the log. Found a PDF file which likely the first document that the attacker got their hands on.

![image](https://github.com/user-attachments/assets/e11321b3-e9f1-49f7-8350-dad2dce66e5c)


> 6TH QUESTION -> ANS: `C:\Users\Dutch\Documents\2025- Board of directors Documents\2025-BUDGET-ALLOCATION-CONFIDENTIAL.pdf`

![image](https://github.com/user-attachments/assets/4ef005ed-b067-4ce2-a25d-2ab5a34346d9)

16. Found another PDF that should be the second stolen document.

![image](https://github.com/user-attachments/assets/f2859c25-7421-4bf8-8633-49a1e197b6c4)


> 7TH QUESTION -> ANS: `MEGAsync`

![image](https://github.com/user-attachments/assets/f3395436-e559-407e-9492-d49d2f85855d)

17. To identify the installed cloud utility used to steal and exfiltrate the documents, we just need to continue review the same event log file.
18. Found a downloaded setup binary for **MEGAsync** and not long after that you shall identify **MEGAsync.exe** binary execution.

![image](https://github.com/user-attachments/assets/b14aac96-b8a7-47b7-9e43-7350629ed0b3)

![image](https://github.com/user-attachments/assets/9cbd12fc-54dd-4530-9a6c-f1f2c4bec039)

> 8TH QUESTION -> ANS: `2025-01-24 10:22:19`

![image](https://github.com/user-attachments/assets/94f03be4-af63-43e0-97f2-318d024f1e8d)


19. Again, based on our previous finding, we can identify the timestamp for this utility execution is at `2025-01-24 10:22:19`. 


> 9TH QUESTION -> ANS: `File Shredder`

![image](https://github.com/user-attachments/assets/51b7cb02-4139-4415-8c7b-dfd45d9a9203)


20. Again, while continuing the review. Found a binary execution named **File Shredder** at timestamp `2025-01-24 10:26:40`. A file shredder is a specialized tool that permanently deletes files by overwriting them multiple times.

![image](https://github.com/user-attachments/assets/0da79142-aca7-4873-b024-353a3f76bee9)


> 10TH QUESTION -> ANS: `2025-01-24 10:28:41`

![image](https://github.com/user-attachments/assets/2d360039-bf08-4d1a-a261-103c1e6c8016)


21. To identify an attempt to clear log files, we need to check the **Security** event log and filter for eventID **1102**.

![image](https://github.com/user-attachments/assets/0e133d84-42c2-4466-a31d-fb0913504acf)

22. Now we know the timestamp for log clear activity is at `2025-01-24 10:28:41`.
23. Great! We've investigated the case.

## IMPORTANT LINKS:

```
https://ponderthebits.com/2018/02/windows-rdp-related-event-logs-identification-tracking-and-investigation/
https://s0cm0nkey.gitbook.io/s0cm0nkeys-security-reference-guide/dfir-digital-forensics-and-incident-response/ir-event-log-cheatsheet
https://learn.microsoft.com/en-us/windows/security/operating-system-security/virus-and-threat-protection/microsoft-defender-smartscreen/
https://www.cyfirma.com/research/elpaco-team-ransomware-a-new-variant-of-the-mimic-ransomware-family/
```
