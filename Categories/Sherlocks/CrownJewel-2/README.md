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
> 2ND QUESTION --> ANS: `C:\Windows\Temp\dump_tmp\Active Directory\ntds.dit`
> 3RD QUESTION --> ANS: `2024-05-15 05:39:56`
> 4TH QUESTION --> ANS: `2024-05-15 05:39:58`
> 5TH QUESTION --> ANS: `ESENT`
> 6TH QUESTION --> ANS: `Administrators, Backup Operators`
> 7TH QUESTION --> ANS: `2024-05-15 05:36:31`

## REFERENCE(S):
```
https://wongkenny240.gitbook.io/computerforensics/incident-response-artifacts/volume-shadow-copy
https://attack.mitre.org/techniques/T1003/003/
```
