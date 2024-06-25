# ProcNet
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/16fbee1e-eb57-4c6d-924e-ab9e4649d9cc)


## Lessons Learned:
- asdasda

## SCENARIO:
<p align="justify">With the rising utilization of open-source C2 frameworks by threat actors, our red team has simulated the functionalities of one such widely employed framework. The objective of this exercise is to aid blue teams in strengthening their defenses against these specific threats. We have been provided with PCAP files and APIs collected during the event, which will serve as valuable resources. Using the API Monitor: We are well-acquainted with opening PCAP and .EVTX files, but what are .apmx64 ? The .apmx64 file extension is associated with API Monitor, a software used to monitor and control API calls made by applications and services. To commence your analysis, follow the steps provided below: Download the API Monitor Navigate to "Files" and click on "Open" to view captured data from the file: "Employee.apmx64" or "DC01.apmx64" After opening the file, the "Monitoring Process" window will populate with a list of processes. Expand the view by clicking the '+' symbol to reveal the modules and threads associated with each process. The API calls can be observed in the "Summary" window. To focus our analysis on a specific module, click on the different DLLs loaded by the processes. TIP: When conducting analysis, it is advisable to begin by examining the API calls made by the process itself, rather than focusing solely on DLLs. For instance, if I intend to analyze the API calls of a process named csgo.exe, I will initially expand the view by clicking the '+' symbol. Then, I will narrow down my analysis specifically to 'csgo.exe' by selecting it, and I can further analyze other DLLs as needed.</p>

## STEPS:
1. In this case, we're tasked to..

> 1ST QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dd26f63f-3fd6-4803-9775-03de3b159bac)


> 2ND QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4bae8c80-4397-48e4-8f0d-acb16e5b1d0c)


> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5f313be4-67e3-4350-b2e5-1cba3a76de95)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5ed6afbb-89d6-47c6-a67d-087029e953bb)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/367afea3-2d47-40f4-b98f-900446b4faca)



> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0f6cc847-2168-47f3-815c-d71e492408eb)



> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1a6fe32c-8e06-45ec-908a-d53f7bb0cd81)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/65fea4f2-6ac7-4a03-a0d8-75f3ef57ed75)


> 9TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4d575e0f-d00c-42a6-8dd6-9960a9b75785)


> 10TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cb095d06-161f-40fe-8ac1-527de6b1aac2)


> 11TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bb39097d-b1a7-4332-b438-6f7dcc5fcc2d)


## IMPORTANT LINKS

```
```
