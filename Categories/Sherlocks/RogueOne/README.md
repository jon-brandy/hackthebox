# RogueOne
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8a7c34cc-784b-4e1c-b9d4-baf9d3433187)


## Lessons Learned:
- Using volatility3 to conduct memory forensics.

## SCENARIO:

Your SIEM system generated multiple alerts in less than a minute, indicating potential C2 communication from Simon Stark's workstation. 
Despite Simon not noticing anything unusual, the IT team had him share screenshots of his task manager to check for any unusual processes. 
No suspicious processes were found, yet alerts about C2 communications persisted. The SOC manager then directed the immediate containment 
of the workstation and a memory dump for analysis. As a memory forensics expert, you are tasked with assisting the SOC team at Forela 
to investigate and resolve this urgent incident.

## STEPS:
1. In this challenge we're given a memory dump which we can analyze using volatility.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c9bf2516-20ec-429e-9b5c-8a25f2fcad23)



> 1ST QUESTION --> ANS: 6812

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/989f7f08-c3a9-499f-9f74-af9304baa108)


2. Running a basic file check to identify what OS memory we're dealing with, shall resulting to **windows**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7bc4e6ec-60fc-4ddb-94f5-6aff07c943d1)


3. Hence we can use windows plugin using volatility.

### Looking for IOCs

4. Let's check for connections that are active at the time of the memory dump process.

```
Why looking for active connections?
-> Remembering the scenario said there is potential for C2 Communication from Simon Stark's workstation. Hence, it's easier for us to
identify the malicious process by checking active connections.
```

```
python3 ../../volatility3/vol.py -f 20230810.mem windows.netstat
```


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4e6cee69-0a26-44fb-8670-27908155ada2)


5. Based from the results, the top 7 shall be our interest here. Because the rest mostly just being unestablished connections waiting for another user to connect.
6. Noticed one **svchost.exe** process standing out as communicate with uncommon port.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d20263ae-6222-4cc4-9cb3-6eb1bf44e15f)


7. At this point, it's quite clear that the malicious PID is --> `6812` but to support our arguments, we can try to check parent process and child process for the top 7.

```
python3 ../../volatility3/vol.py -f 20230810.mem windows.pstree | grep -E '6136|8224|6812|8224|3404|8224|3404'
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/210ce734-7772-481e-8530-36517cfcbb87)


8. Great! 6812 indeed is the malicious PID, because cmd.exe comes out as the child process from the svchost.exe for the specified PID.
9. Not only that, we can identified another anomaly that the parent for the malicious svchost.exe is different than the other svchost.exe parent.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6f4b109a-cb2f-49ed-a8c7-899593a1cbbf)


10. Checking for PID 7436 shall resulting to **explorer.exe** (File Explorer).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/70e71aa4-24c8-4885-bfa8-ab0f3cd4aed9)


11. Nice! It is clear that PID 6812 is the malicious process.

```
How come svchost.exe becomes the malicious process?
--> As we know svchost.exe (Service Host) is a process used by windows to run or handle DLLs that the device needs to execute.
Knowing this, the attacker might spoof few legitimate processes, one of them is Service Host. 
```


> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/78eb4957-6a6e-4e01-83c5-52ce7faf7f90)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a46b2bd6-153c-4281-94b4-16ce0a8f128d)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/59721088-9c05-4618-919a-b7e727afdee4)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/535cab90-f0d1-4ace-93f3-b767bac4c701)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/49f0b387-c048-40f2-88a3-23b2ab8c4e44)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/baf4d3cd-0517-43f9-a0e7-7d8c6416d516)

