# Netmon
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, let's do nmap.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210515351-571921b4-c807-48c8-81ba-b66341c4f851.png)


![image](https://user-images.githubusercontent.com/70703371/210515384-542e5a38-cdd1-4470-8fce-e857126c91c2.png)


![image](https://user-images.githubusercontent.com/70703371/210515422-c2275f3f-a477-4d4c-994b-58e871ac2e57.png)


2. Based from the result here, we know that **anonymous ftp login allowed** and the machine seems running a web service at port 5985. Not only that there's **SMB** ports open.
3. And it seems there's a vuln with the smb service.

![image](https://user-images.githubusercontent.com/70703371/210516180-3cea3746-0091-4e05-b99e-f0b6d0e8837c.png)

4. Anyway let's login with ftp.

> RESULT - INFORMATION GATHERING

![image](https://user-images.githubusercontent.com/70703371/210516407-cb5ee042-3e12-40a1-8aaf-d309e88e84ff.png)


![image](https://user-images.githubusercontent.com/70703371/210516445-6ec237bd-8550-4dc1-823c-81ad8e10a855.png)


![image](https://user-images.githubusercontent.com/70703371/210516710-a32fac3a-a666-46df-b9b6-d855f0aa08a0.png)


![image](https://user-images.githubusercontent.com/70703371/210516750-e773400e-65d5-41d6-81b6-e14edbcbd541.png)


![image](https://user-images.githubusercontent.com/70703371/210516785-75a72644-10a3-4989-97af-0ed17e773d64.png)


![image](https://user-images.githubusercontent.com/70703371/210516936-ac7055ce-6080-4706-8176-ec321f9b9d90.png)


5. Notice there's `user.txt` file, let's download that.

![image](https://user-images.githubusercontent.com/70703371/210517122-e8d0f1ac-1279-4e2c-a2f3-ec75e44ece6a.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/210517197-ae0fb438-3f11-4b5b-8af4-4c001cfcbdf0.png)


## USER FLAG

```
607cf9cc7557252d24df4bff40865833
```

6. Now let's open the host in the web browser.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210517823-d835fee1-1379-4a99-9d00-e259b97c3732.png)


7. I did a small outsource about `PRTG Network Monitor (NETMON) default credentials`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210518436-f250da93-5984-46b6-b3fb-b5b669126059.png)


```
https://www.192-168-1-1-ip.co/router/prtg/prtg-network-monitor/16981/
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210519289-7f927449-fae6-4586-8aab-9d28f87888a1.png)


8. Hmm.. Let's check any backup files available (?)

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210520043-e9ae9f9c-acda-43f9-a189-0c7bb4dc95ca.png)


9. Let's jump to `programData`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210520153-57fe1747-9fd7-442b-9692-6dc1a6125cc1.png)


10. The `Paessler` directory called my attention.
11. Let's jump there.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210520534-36db027f-f7e7-47c0-bcf0-f16b820a6098.png)


![image](https://user-images.githubusercontent.com/70703371/210520607-70fec31b-1b69-4bfa-9227-631c40ee9aaa.png)


12. Notice there's a backup file, download the `.bak` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210520835-becec9a8-0644-44d5-b4d2-ebe8443f8d76.png)


13. When i **cat** the file, there's a lot of base64 encoded text, but none of what i found gave me the flag or any clue.
14. Anyway i found this tag which has the cred.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210521437-bffe68af-eccd-484e-9611-b87c9b3254c2.png)


```
username -> prtgadmin
password -> PrTg@dmin2018
```

![image](https://user-images.githubusercontent.com/70703371/210521606-b2d55186-5486-4c9a-8af0-8201cd65aeed.png)


15. Still got the wrong cred.
16. I'm stucked here, then i tried to change the year to 2019 (since the box was released in 2019).

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210522597-5ee2e04e-3a89-4671-a5c6-c939c319f74c.png)


17. Got no clue now, let's search for **PRTG Exploit**.

```
https://www.exploit-db.com/exploits/46527
https://github.com/wildkindcc/CVE-2018-9276
```

18. It seems we can copy the root.txt file to the public repository by this command:

```
Copy-Item -Path "C:\Users\Administrator\Desktop\root.txt" -Destination "C:\Users\Public\root.txt" -Recurse
```

19. Anyway there's another way to get the `root.txt` file, you can run `searchsploit prtg` to find another approach.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210527327-efe30d4f-e4d5-45ba-8149-ca4127840553.png)


![image](https://user-images.githubusercontent.com/70703371/210527460-b84773c9-cb66-461b-bcce-8de4c6ff0c99.png)


21. Let's copy the script to our directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210527639-2bfe4558-96ea-4944-bd6b-abd0994caaa7.png)


![image](https://user-images.githubusercontent.com/70703371/210527732-924b3d9c-eb89-4f04-8742-07dd79569c01.png)


22. We can see there's a guide.

![image](https://user-images.githubusercontent.com/70703371/210527857-de864b26-619b-4c5b-9059-f123b8d222d7.png)


![image](https://user-images.githubusercontent.com/70703371/210527885-bb2ac3cc-2e22-4741-b1d3-f4d1dfe73047.png)


23. Let's go back to our first approach, open the web app again, go to setup -> account settings -> notifications.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210529284-6edb0356-8e0c-4958-a8ca-9fe73f555f1a.png)


24. Choose `add new notification` and change the `Notification name` to **New Notification**.

![image](https://user-images.githubusercontent.com/70703371/210529829-a326963d-f08d-4fbc-97e5-9b804bf2ef5b.png)


25. Choose the `Execute Program`.

![image](https://user-images.githubusercontent.com/70703371/210529889-9584851d-0af9-4b56-a45a-dbbccb52f51c.png)


> Choose the output file to outfile.ps1

![image](https://user-images.githubusercontent.com/70703371/210530094-dd4d88bc-73e7-491f-ad72-1acdee7ff106.png)

> Fill the parameter with this

```
flag.txt; Copy-Item -Path "C:\Users\Administrator\Desktop\root.txt" -Destination "C:\Users\Public\root.txt" -Recurse
```

26. Click save!
27. Now open the ftp again, then choose the bell symbol at the notification's name.

![image](https://user-images.githubusercontent.com/70703371/210530573-9aec385c-72ad-4e2d-bc08-20fe269c08d0.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/210530636-c18197f9-842c-4b53-9317-488798f4f4ee.png)


28. Download the `root.txt` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210530779-c75093d2-d407-45ec-9f3a-300a5a0ffbf2.png)


## ROOT FLAG

```
4b0f0ae842643eb2251cc83372cf48b2
```

