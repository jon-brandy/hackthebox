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


> 2ND QUESTION -> ANS: `WinRAR`

![image](https://github.com/user-attachments/assets/50b412a0-82a6-4f18-954f-d61ded782e47)


> 3RD QUESTION -> ANS: `C:\Users\Dutch\Downloads\Everything.exe`

![image](https://github.com/user-attachments/assets/cd70cd64-c2d5-4178-939b-e9db77473350)

> 4TH QUESTION -> ANS: `2025-01-24 10:17:33`

![image](https://github.com/user-attachments/assets/6b3be03d-d7c0-4883-9ca9-5cc49bfc4fad)


> 5TH QUESTION -> ANS: `C:\Users\Dutch\Documents\2025- Board of directors Documents\Ministry Of Defense Audit.pdf`

![image](https://github.com/user-attachments/assets/94d2b3ef-8add-4d7e-a267-1ba5670d2263)


> 6TH QUESTION -> ANS: `C:\Users\Dutch\Documents\2025- Board of directors Documents\2025-BUDGET-ALLOCATION-CONFIDENTIAL.pdf`

![image](https://github.com/user-attachments/assets/4ef005ed-b067-4ce2-a25d-2ab5a34346d9)


> 7TH QUESTION -> ANS: `File Shredder`

![image](https://github.com/user-attachments/assets/f3395436-e559-407e-9492-d49d2f85855d)


> 8TH QUESTION -> ANS: `2025-01-24 10:28:41`

![image](https://github.com/user-attachments/assets/94f03be4-af63-43e0-97f2-318d024f1e8d)


> 9TH QUESTION -> ANS:

![image](https://github.com/user-attachments/assets/51b7cb02-4139-4415-8c7b-dfd45d9a9203)


> 10TH QUESTION -> ANS:

![image](https://github.com/user-attachments/assets/2d360039-bf08-4d1a-a261-103c1e6c8016)


## IMPORTANT LINKS:

```
https://ponderthebits.com/2018/02/windows-rdp-related-event-logs-identification-tracking-and-investigation/
```
