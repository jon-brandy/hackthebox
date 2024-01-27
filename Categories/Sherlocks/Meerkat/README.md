# Meerkat

> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/860f1cb2-71d0-48c5-bb58-9cf4d6155baa)

## Lesson learned:
- Identifying **Credential Stuffing** attacks.
- Bonitasoft CVE.
- Packet filtering and custom column value.

## SCENARIO:

<p align="justify">

As a fast growing startup, Forela have been utilising a business management platform. 
Unfortunately our documentation is scarce and our administrators aren't the most security aware. 
As our new security provider we'd like you to take a look at some PCAP and log data we have exported to confirm if we have (or have not) been compromised.

</p>

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

> 6TH QUESTION --> ANS: seb.broom@forela.co.uk:g0vernm3nt

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a082e00a-fee4-4836-89a8-7948ad0238de)


25. To answer this, we can filter the response which status code is below 300. Filter command --> `http.response.code < 300`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b72c169-87c9-4aa9-886a-0ee980fb440a)


26. After analyzing each log, seems only the packets with status code 204 which is a response of the login request. 204 indicates the server has successfully fulfilled the request and that there is no additional content to send in the response payload body.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/273c09ff-bc18-4c0f-b5f4-922b21665150)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3edb78c7-4bee-435f-9448-36e2cf4fbbb1)


> 7TH QUESTION --> ANS: pastes.io

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c6abcaa5-5571-4df8-8d67-5762ac50a52c)


28. To answer this, we can simply filter the packet using --> `http.request.method`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3cfc4e39-daed-47a5-9271-4530c871c6a4)


> 8TH QUESTION --> ANS: 0dc54416c346584539aa985e9d69a98e

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d5ed6fb7-ac2e-47bd-b693-a48da008eed1)


29. To get the hash, we need to export the objects of our previous packet.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eea286b6-0b0f-4074-8d34-95f7c3a4cb7d)


30. Running **file** command it states that the exported objects is a JSON data.
31. Reading it shall found the endpoint of the script used by hacker, run wget shall download the script.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9de08475-1899-45ff-925e-23402d4cacd9)


32. To get the md5checksum simply run **md5sum**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1df562b2-302c-47cb-9d2f-e51c6057f881)


> 9TH QUESTION --> ANS: dbb906628855a433d70025b6692c05e7

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c85d9716-5f52-4e87-88dc-aed615f641a8)


33. Accessing the pastes.io shall resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ed05bbff-f1be-4ef4-a713-42b092255d0f)


34. Based from the bash script, we can identified that `hffgra4unv` contains the public key.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/59441f05-fadc-4ef3-a5d4-0b00aa29f995)


35. Simply `wget` it then get the md5sum.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/27b045a1-fcc4-4fed-83c3-952032bec332)


> 10TH QUESTION --> ANS: /home/ubuntu/.ssh/authorized_keys

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ed956922-19d9-42ae-8760-d4814197e955)


36. The answer is the destination of the public key.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b9580b7e-897e-4308-91ff-0c977443f74e)


> 11TH QUESTION --> ANS: T1098.004

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d2d19336-38b0-4409-8b2a-aafa68f3d810)


37. Searching `ssh` shall resulting to these:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/220d379e-205f-42ae-a56a-8876d054ba03)


38. The first one should be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e49d3285-e0b2-408a-8cac-f505f927e4d4)


39. It discussed the same method used by the attacker.

### IMPORTANT LINKS:

```
https://nvd.nist.gov/vuln/detail/CVE-2022-25237
https://attack.mitre.org/techniques/T1110/004/
```
