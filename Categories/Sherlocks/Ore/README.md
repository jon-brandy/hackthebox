# Ore
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/008e35c8-a398-44a2-a5d1-b81a7a1e4ada)

## Lessons Learned:
- Reviewing Grafana and Catscale Output artifacts.
- Analyzing xmrig process.
- Hunting the Threat Actor's IPs by reviewing UNIX auth log, Web server log, and UNIX sysmon log (syslog).

## SCENARIO:
<p align="justify">One of our technical partners are currently managing our AWS infrastructure. We requested the deployment of some technology into the cloud. The solution proposed was an EC2 instance hosting the Grafana application. Not too long after the EC2 was deployed the CPU usage ended up sitting at a continuous 98%+ for a process named "xmrig". Important Information Our organisation's office public facing IP is 86.5.206.121, upon the deployment of the application we carried out some basic vulnerability testing and maintenance.</p>

## STEPS:
1. In this case, we're tasked to investigate an anomaly that happened in Forela's AWS infrastructure. The infra itself is managed by a technical partner of Forela.
2. It is known that the CPU usage of the deployed EC2 instance unexpectedly soared to a constant of 98%+ due to a process named "XMRIG". The EC2 instance was used to host Grafana application.
3. As a cyber forensic, wr're tasked to investigate what "XMRIG" is due to our understanding about cloud infrastructure, EC2 instances, and system processes.

> 1ST QUESTION --> ANS: CVE-2021-43798

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a83b0a5f-0659-41af-99fd-8ce47e5d75fd)


3. Upon reviewing the Grafana artifacts, the Grafana's version used is shown at the `VERSION` file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d01dac73-5803-4e74-b34e-ccb81cc30528)


4. Searching on the internet for CVE related to the version, we found these results.

> RESULTS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0784d0cb-81c6-447f-a43e-7067525a429d)


5. Reviewing each of them, drop us to a conclusion of the related CVE to this version should be --> `CVE-2021-43798`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b259768-99c3-4edb-9bdc-2b3d0a195d5b)


> 2ND QUESTION --> ANS: 44.204.18.94,95.181.232.32,195.80.150.137

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/215bb639-0ccc-42b6-a0b7-6fd5b60b9207)


6. Now let's review the catscale output.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/817bd491-6db8-41e8-9dea-9fa25b4b8dbf)


#### NOTES:

```
LinuxCatScale is a bash script that uses live of the land tools to collect extensive
data from Linux based hosts.

The data provided can help DFIR professinoals in triaging and scoping incidents.
The output from LinuxCatScale typically includes detailed reports on vulnerabilities,
configuration issues, and an overall security score to help administrators quickly understand
and address security weaknesses.
```

7. Navigating to the `/Logs` directory, we found 2 .gzip files. The var log should be our interest. Let's extract it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cf0a2448-659e-4137-92e2-d693054af189)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/08958846-c73a-4fa3-b340-035f6b63617b)


8. Our investigation shall start at the UNIX auth log. Based from the scenario, we know that IP 86.5.206.121 is a legitimate IP. It's Forela's public IP.
9. Hence, every IP starting with 86.x.x.x shall ignored.
10. Upon reviewing the auth log, found several IPs attempt to establish a connection to port 22 but is dropped by the system. It failed to connect.

> ONE OF THEM --> At `12:14:50 - 12:14:51`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b36b6f92-d52c-49c9-abe5-d7e3b2fb994f)

#### NOTES:

```
The failed pre-auth behavior is often indicative of automated scanning or probing activity. It's a good practice to monitor
such activities and take preventive measures if necessary.
```

11. Upon further check about the IP. We found that the IP is registered as "Bad Reputation IP" with abuse reports of 15,037 times.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9b6007de-864c-4912-ac3c-cbfd785a7859)


12. But we can't jump to a conclusion yet that it's the one that compromised the Forela's organization. Because there are bunch other failed logon with Bad Reputation IP.

13. Long story short, one IP caught my interest --> `195.80.150.137`. It's stuffed few creds at `10:59:12 - 11:08:09`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ebfebec5-c4c9-4282-81c9-5856f6ca4ee7)


14. But then it authenticated as `grafana` at `11:17:18`. Nice, we hunted one IP then. The rest IP are still the suspect.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/88feca18-1fcf-40b5-8052-ca89e1dfacfc)

> SMALL DETAILS ABOUT THE IP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/07da419c-c2fc-47d2-bc9f-61b9dff06170)


15. Now, let's review the `Process_and_Network` and let's query brutally for XMRIG process. We just want to get more information about the XMRIG activities at the EC2.

> RESULTS - Got few interesting informations.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/193efa2b-116a-402b-981f-69c4d5af8295)

16. Great! Based from the results above, we confirm that we can see a process named XMRIG running from `/usr/share/logs.txt/`.
17. Now let's move to the grafana directory and review the logs at `/usr/share/grafana/data/log/`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9c3860e5-21f9-43a9-b208-79b71f4298f0)


18. Upon reviewing each logs, we will find several False Positive activity. Remembering the Forela currently running VA and maintenance to the server.

> FALSE POSITIVE IP --> each IP started with 86.x.x.x or IP with the same beginning 3 blocks.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d824a932-64d6-42a6-ad1a-612ac1654e18)


19. Long story short, found another IP that attempted arbitrary file read.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/160de78c-a1d0-4bb4-b363-b504e2e5060f)


> SMALL DETAILS ABOUT THE IP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d0f529d3-3deb-4d4d-9420-45fa09bb0711)


20. Then found 2 other IPs accessing `/login` endpoint. One of them is has reported for ABUSE IP --> `44.192.62.21`. This should be our suspect.
 
![image](https://github.com/jon-brandy/hackthebox/assets/70703371/82aa39a8-27b2-49c8-969e-67a40a7110a7)


> SMALL DETAILS FOR `44.192.62.21`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c6fd73b4-4a69-4a32-9b62-166ecf64b288)


21. At this point, it's proven for the first 2 IP is the threat actor's IP. Now we need to prove this potential last suspect IP.
22. Let's continue our investigation by reviewing the Linux Sysmon logs. Actually I did not have the setup for ELK stack or splunk. So it's kinda hard to analyze it in raw logs.
23. I highly recommend setup an ELK stack then import the log or using splunk to review the log.
24. Upon reviewing the raw log **manually**, at 24th November `08:30:01` found an attempt to use command `wget` at the machine.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ae60b26-2248-444b-ab1c-3ec3503532bb)


25. Based from our previous auth.log identification, IP `195.80.150.137` logged in to the EC2 server as grafana at 23th November, then do login and logout few times.
26. At the next day, seems the attacker tried to import **injection.sh** file from his web server --> `44.204.18.94`.
27. Reviewing the rest syslog, found no other malicious activity or IP that seems connected with the 2 previous IP we hunted.
28. Great! Seems we hunted all the threat actor's IPs.


> 3RD QUESTION --> ANS: grafana

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fb666590-22e3-46ab-b8e1-4aeda573da07)

29. Based from our previous finding. It's clear that the attacker utilize **grafana** user to infiltrate to the system.

> RECAP EVIDENCE FROM AUTH LOG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1646d79b-4d2d-4fb2-9e7c-2286f4d770b5)


30. There are no other user login activity detected based from the auth log.

> 4TH QUESTION --> ANS: /opt/automation/updater.sh

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c06d69a4-fe98-4513-966d-b003e7414f39)

31. Surprisingly, if we review again the log which contains the wget command. Noticed the user value is already as **root**. Not **grafana**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a8a37216-a6e2-4ff5-b2c5-9d790649f7b4)


32. This mean, the attacker escalated privileges. Interestingly, a bash script is executed --> updater.sh.
33. When reviewing the other syslog file --> syslog.1. We found **nano** and **cat** command execution for file **updater.sh**.

> CAT EXECUTION - 24TH NOVEMBER `11:27:43` - USING GRAFANA USER

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6f091837-9b2c-438d-9a4c-36b82b9548eb)


> NANO EXECUTION - 23TH NOVEMBER `11:45:50` - USING GRAFANA USER

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ef82c170-c624-4bad-8c16-2f29e249e6e5)


34. At this point, we can speculate an attempt for modifying a bash file that could be a cronjob file. Because it gets executed as root at the `/opt/automation/updater.sh` file.
35. To check for cronjob activity, let's traverse to `Persistence` directory.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0eb8950c-e373-4d7e-adc6-4f2520dc0e5f)


36. Checking the **cron-tab-list**, `/opt/automation/updater.sh` listed as a cronjob file. At this point, it's clear the attacker intention, he tried to escalate privilege by tampering the `updater.sh` file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8549265d-a613-408b-8d3e-4006ec57c9bb)

> 5TH QUESTION --> ANS: wget

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a4bca183-54a5-42ac-ae59-eaaae9304e56)


37. After the attacker gained privesc, previously we identified he tried to download another bash script named **injector.sh** using **wget** command.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/04ec8773-797a-435e-b020-95b9442b9358)


> 6TH QUESTION --> ANS: /opt/automation/

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/267a1ade-f604-466c-870c-8e15e48a63a2)


38. Scrolling down below, the attacker execute a **curl** command which used to download the XMRIG (mining binary) and the config file.
39. Based from the **CurrentDirectory** parameter, it's clear that both files initially downloaded to `/opt/automation`.

> 24TH NOVEMBER `09:59:47`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/528f47e4-ee0d-403b-87ba-4d0a92301dcc)


> 7TH QUESTION --> ANS: curl

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df8aea36-be13-497e-aa09-bb3acc8b61a7)


40. Again, still from our previous identifications. The attacker using **curl** command to download both the crypto mining binary and the config file.



> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/28f31da6-a23f-42e6-8d00-c177374db3bd)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d807380d-67a5-4327-9081-020ca2b05c40)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cd6e1342-9d44-44aa-96d8-652531693d1f)


> 11TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/250bdae2-45b4-4e82-a44b-208640d673fa)


> 12TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58dbbdaf-3c95-482b-9d90-f1036a6dee36)


> 13TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ab23efbd-6abb-4ac0-8d25-3ff2a92a22c0)


> 14TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1c04868c-0311-48e1-9231-af5db3b86fea)


## IMPORTANT LINKS:

```
https://www.cybersecurity-help.cz/vdb/grafana_labs/grafana/8.2.0/
https://github.com/pedrohavay/exploit-grafana-CVE-2021-43798
```
