# CrashDump
> Write-up author: jon-brandy

## Lessons Learned:
1. User-mode debugging with WinDbg.
2. Cobalt Strike.

## SCENARIO:

<p align="justify">A suspicious executable was identified running on one of the compromised endpoints. Initial triage suggests that this process may have been leveraged by the threat actor to establish a foothold on the system. To support further malware analysis and behavioral reconstruction, a user‑mode process dump of the suspected executable has been provided.
</p>

## STEPS:
1. as

> 1ST QUESTION --> ANS: `10.0.10240.16384`

<img width="1326" height="242" alt="image" src="https://github.com/user-attachments/assets/aff48f1c-d520-418c-8abd-773f0e2c3f9b" />

> 2ND QUESTION --> ANS: `C:\Users\s1rx\Downloads\update.exe`

<img width="1327" height="240" alt="image" src="https://github.com/user-attachments/assets/0b908edc-8a01-462a-9a77-bcb99de835ad" />


> 3RD QUESTION --> ANS: `6`

<img width="1325" height="239" alt="image" src="https://github.com/user-attachments/assets/6e850220-e3b8-4bbf-8948-5ac9cd972c91" />


> 4TH QUESTION --> ANS: `MSSE-1641-server`

<img width="1327" height="239" alt="image" src="https://github.com/user-attachments/assets/d19cd0f8-c828-486b-a885-330484475111" />


> 5TH QUESTION --> ANS: `2336`

<img width="1329" height="240" alt="image" src="https://github.com/user-attachments/assets/153992d7-d855-40c9-be53-794caf991653" />


> 6TH QUESTION --> ANS: `2025-11-05 01:09:12`

<img width="1326" height="242" alt="image" src="https://github.com/user-attachments/assets/71e119a6-90f9-497d-a1b5-f52bbccab708" />


> 7TH QUESTION --> ANS: ``b1`20870000``

<img width="1328" height="241" alt="image" src="https://github.com/user-attachments/assets/078c7853-cc44-4bb6-ac58-a58c55825a28" />


> 8TH QUESTION --> ANS: `101.10.25.4`

<img width="1326" height="241" alt="image" src="https://github.com/user-attachments/assets/e491db15-09ee-4437-b3bf-e97832236e8f" />


> 9TH QUESTION --> ANS: `Cobalt Strike`

<img width="1328" height="242" alt="image" src="https://github.com/user-attachments/assets/5dbce35b-9bd1-4f75-857c-c7c1ce547bc1" />


## REFERENCES:

```
```
