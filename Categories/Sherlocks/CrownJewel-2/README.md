# CrownJewel-2
> Write-up author: jon-brandy

<img width="422" height="161" alt="image" src="https://github.com/user-attachments/assets/7d0ae2fd-3aae-43fd-a00a-992b794b347b" />


## Lessons Learned:
1. Use `Hayabusa` to parse forensic artifacts and flag malicious activity.
2. Use `EvtxECmd` to parse Windows Event Logs.
3. Use `Timeline Explorer` to analyze the parsed event logs.
4. Analyze NTDS dumping activity and enumeration of privileged user groups.

## SCENARIO:
<p align="justify">Forela's Domain environment is pure chaos. Just got another alert from the Domain controller of NTDS.dit database being exfiltrated. Just one day prior you responded to an alert on the same domain controller where an attacker dumped NTDS.dit via vssadmin utility. However, you managed to delete the dumped files kick the attacker out of the DC, and restore a clean snapshot. Now they again managed to access DC with a domain admin account with their persistent access in the environment. This time they are abusing ntdsutil to dump the database. Help Forela in these chaotic times!!</p>

## STEPS:
1. sad

> 1ST QUESTION --> ANS: `2024-05-15 05:39:55`

<img width="1281" height="227" alt="image" src="https://github.com/user-attachments/assets/fa66567b-cabd-48e5-a59a-8eb700374c3e" />


> 2ND QUESTION --> ANS: `C:\Windows\Temp\dump_tmp\Active Directory\ntds.dit`

<img width="1282" height="204" alt="image" src="https://github.com/user-attachments/assets/0fc34789-6565-4abb-9474-ba9f0f4611bd" />


> 3RD QUESTION --> ANS: `2024-05-15 05:39:56`

<img width="1279" height="204" alt="image" src="https://github.com/user-attachments/assets/0827239d-73e8-469c-ae5d-ecf1442af855" />


> 4TH QUESTION --> ANS: `2024-05-15 05:39:58`

<img width="1285" height="203" alt="image" src="https://github.com/user-attachments/assets/353eb3b5-ab50-441e-8e0b-179d4bc51701" />


> 5TH QUESTION --> ANS: `ESENT`

<img width="1281" height="204" alt="image" src="https://github.com/user-attachments/assets/c7bea1a2-4a7e-4177-8313-3a88a2158106" />


> 6TH QUESTION --> ANS: `Administrators, Backup Operators`

<img width="1280" height="227" alt="image" src="https://github.com/user-attachments/assets/7e39dc84-9c14-4d04-8bd5-a958e0bafd29" />


> 7TH QUESTION --> ANS: `2024-05-15 05:36:31`

<img width="1284" height="205" alt="image" src="https://github.com/user-attachments/assets/32e4163a-b576-40c3-bc35-726f947716c2" />


## REFERENCE(S):
```
https://wongkenny240.gitbook.io/computerforensics/incident-response-artifacts/volume-shadow-copy
https://attack.mitre.org/techniques/T1003/003/
```
