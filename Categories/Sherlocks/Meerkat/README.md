# Meerkat

## Lesson learned:
- Identifying **Credential Stuffing** attacks.
- Bonitasoft CVE.
- 

> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/860f1cb2-71d0-48c5-bb58-9cf4d6155baa)


## DESCRIPTION:
As a fast growing startup, Forela have been utilising a business management platform. 
Unfortunately our documentation is scarce and our administrators aren't the most security aware. 
As our new security provider we'd like you to take a look at some PCAP and log data we have exported to confirm if we have (or have not) been compromised.

## STEPS:
1. In this challenge we're given two files.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/317a7617-95f3-4020-8255-a3676d20bec2)


> 1ST QUESTION --> ANS : Bonitasoft.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/633d94c8-2997-4a84-9322-8728099a8d4d)


2. To answer it, I started by analyzing the .pcap file.
3. Found out that there are several request with POST method to `172.31.6.44`. The endpoint is `/bonita/loginservice`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58833602-a454-4e6b-a30c-6c97080f7369)


5. Searching for **Bonita** at the .json file, shall resulting to `Bonitasoft`. Great now we know the ans is `Bonitasoft`.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3034bbfd-bbfc-4212-9836-1b942ef56356)


> 2ND QUESTION --> ANS: Credential Stuffing.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ec6d3311-5945-4c30-a9f9-c011c290035c)


6. Continue analyzing the logs, noticed several response with status code **401** which indicates **unauthorized access**.
7. I tried to follow few of them and found several different creds used.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7d8c3782-3076-42d3-a6b5-a912ddec0d8a)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d5abd805-6e65-42f5-8956-c72436d4d100)


8. If you noticed, the mail which used as the username always ends with `.forela.co.uk`. This indicates a company email.
9. Remembering status code is 401 for both (actually more), it means the attacker is bruteforcing.
10. The passwords also seem to be specific (?) and few of them seem to be complicated.
11. This kind of attacks is called `Credential Stuffing`.


> 3RD QUESTION --> ANS: CVE-2022-25237.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0cc41dd3-2c10-4ec4-87fd-2fc195ccb627)


12. Searching for keyword **CVE** at the .json file shall found the answer for this.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/947e6bb3-1889-480c-81ff-f98da273b357)



> 4TH QUESTION --> ANS: i18ntranslation

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9b7642b5-815a-4e01-8d42-8c6a630ff50a)


13. Reading the CVE documentation, shall found a statement that the attacker is appending `;i18ntranslation or /../i18ntranslation/` to the end of an URL.


> 5TH QUESTION --> ANS: 56

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c3e0450c-c31d-4693-a40a-b73baab13a37)


14. To get the answer, a filter command is needed for quick analyze.
15. Simply execute --> `urlencoded-form.key == "username"`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1cafdb73-f1e5-4f78-a295-81109b3c916a)


16. To see the username value, luckily wireshark allows us to do custom columns.
17. Hence we can create a custom column --> `edit -> preferences -> columns`, then set the column type to custom.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2450c106-ca85-42ce-a3d5-900f1efa1320)


18. Next, to modify the column, right click at the column area then choose `edit column` and set the fields to --> `urlencoded-form.value`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7748be57-7733-4eee-a154-dab256532790)


19. Noticed at the bottom right it states 118 data displayed.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/73094f81-e60f-488d-8441-70e7273f5e11)


20. Scrolling down the packets, noticed several packets which unnecesarry is included.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b07bf323-3b69-46af-8eaa-96a07f89090e)


21. Hence let's add another filter which denied `install`.
22. Filter command --> `urlencoded-form.key == "username" && !(http contains "install")`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5a4083b4-f3ee-460f-8b8e-1ce28c7a6ee2)


23. Now it shows 59 but there are still duplicated username.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9b85f32c-c9e8-4853-a90d-1e95f2c886b0)


24. Hence the answer is 59 - 3 --> 56.

> 6TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a082e00a-fee4-4836-89a8-7948ad0238de)


25. 




### IMPORTANT LINKS:

```
https://nvd.nist.gov/vuln/detail/CVE-2022-25237
https://attack.mitre.org/techniques/T1110/004/
```
