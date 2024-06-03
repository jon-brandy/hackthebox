# Ore
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/008e35c8-a398-44a2-a5d1-b81a7a1e4ada)

## Lessons Learned:
- Reviewing Grafana and Catscale Output artifacts.
- Analyzing xmrig process.
- 

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


4. Searching on the internet for CVE related to the version, we found these results:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0784d0cb-81c6-447f-a43e-7067525a429d)


5. Reviewin each of them, drop us to a conclusion of the related CVE to this version should be --> `CVE-2021-43798`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/acd7f3c0-c05a-4f47-879e-935347bce16c)


> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/215bb639-0ccc-42b6-a0b7-6fd5b60b9207)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fb666590-22e3-46ab-b8e1-4aeda573da07)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c06d69a4-fe98-4513-966d-b003e7414f39)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a4bca183-54a5-42ac-ae59-eaaae9304e56)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/267a1ade-f604-466c-870c-8e15e48a63a2)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df8aea36-be13-497e-aa09-bb3acc8b61a7)


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
