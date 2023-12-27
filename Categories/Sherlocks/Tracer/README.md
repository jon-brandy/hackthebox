# Tracer
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6a82121a-8a9f-4c90-8b4d-d8e12adaf889)


## Lessons learned:
- Analyzing windows event log file.

## SCENARIO:
A junior SOC analyst on duty has reported multiple alerts indicating the presence of PsExec on a workstation.
They verified the alerts and escalated the alerts to tier II. As an Incident responder you triaged the endpoint for artefacts of interest.
Now please answer the questions regarding this security event so you can report it to your incident manager.

## STEPS:
1. In this challenge we're given few files of windows event log and prefetch files.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/41106a98-cdf9-4eaa-b2d6-0999af903523)


> 1ST QUESTION --> ANS: 9

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e9ab6274-0181-4426-ba61-8cf85ecff92c)


2. To identify how many times was PsExec executed by the attacker, we need to analyze the **Security** event log file.
3. Analyzing the content of the latest log, we can identified the attacker's binary filename.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3aef0425-ecfd-4bc4-baa9-3aa341b907ed)


4. As you can see, it states **Caller Process Name**, it means the result is executed using this binary.
5. Hence, to check how many times it executed we just need to filter the **Event ID** displayed to --> **4625**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eebf76f1-8077-4466-b241-e4e838c7a056)


6. I count it manually, by reviewing each contents. Counted +1 if psexesvc.exe executed.

> 2ND QUESTION --> ANS: psexesvc.exe

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/73d2c743-4d79-426c-abb1-25899b40faca)


7. Based from our previous identification, we identified the binary filename is --> psexesvc.exe.

> 3RD QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/434c9c70-fa2c-4d25-802b-bb2bd5a1a8b2)


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dcf41fa7-96ef-4a73-ac31-d3345953e04b)


> 5TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b21dc320-cf6b-4761-aa1f-e063478c116f)


> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5554716f-12c1-4546-b9b1-1aa1838027ec)


> 7TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0406686d-fdd5-4d64-83c5-a3b8c2fcceab)


