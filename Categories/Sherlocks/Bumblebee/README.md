# Bumblebee
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cff2ee5e-4bfa-4d5b-90e3-a45e4e3516bb)

## Lesson learned:
- Analyzing sqlite3 file.

## SCENARIO:
An external contractor has accessed the internal forum here at Forela via the Guest WiFi and they appear to have stolen credentials for the administrative user! 
We have attached some logs from the forum and a full database dump in sqlite3 format to help you in your investigation.

## STEPS:
1. In this challenge, we're given 2 files. A log file and a sqlite3 file.

> 1ST QUESTION --> ANS: apoole1

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e9d36caf-e15b-4127-ab16-45c2075aec86)


2. To get the username of the external contractor, we can start by accessing the sqlite3 database dump.
3. I start by execute query --> `SELECT name FROM sqlite_master WHERE type='table';`, which resulting to a few results. But one table_name caught should be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3270e1cc-a16a-43ff-ac92-63564c0d6bc4)


4. Execute this query --> `SELECT * FROM phpbb_users;` to check all columns and it's value.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2104f97d-4e3f-4b4b-a1f5-70cdcd54234f)


5. Noticed, there's a username with contractor mail, hence we can identified the external contractor is should be `apoole` or `apoole1`.


> 2ND QUESTION --> ANS: 10.10.0.78

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c5dbeb19-5a56-421c-b2f9-0829b2f68de3)


6. To identify the IP address, we need to just need to check the column value.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9bb56ebc-37ab-4cbe-bb98-25be3fb1377c)


> 3RD QUESTION --> ANS: 9

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/01042a85-d2b1-4942-923b-4837f7b1be44)


7. To find the malicious post that the contractor made, we need to enumerate tables in the database and search for post_id column.
8. Long story short, I found one table that should be our interest, the phpbb_posts table.
9. Noticed at **post_id** 9, the **poster_ip** is the exact same as the contractor's ip.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e2526c1d-65c8-4486-bb38-0035d181e799)


10. Then, analyzing the **post_text** we can intrepret that the contractor post is indeed malicious.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7c997bc2-b940-42e4-be3b-46e109590f7a)


> I'm **SPECULATING** that the contractor tried to do XSS to get users's cookie.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/76c970fe-926c-4942-b46f-f09cb43d0a36)


> 4TH QUESTION --> ANS: http://10.10.0.78/update.php

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e33d8301-d2d9-4a0f-b0ca-771ed0325659)


11. For the URI path, we just need to analyze the malicious content.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ab57f6d7-1d83-4605-9d69-f40bf133ed05)


12. Searching for the attacker's ip address shall gave us the URI path.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/00b9be11-f17f-4d90-a1bc-54a211fcc579)


```
Why searching for the attcker's IP?
-> Since I am SPECULATING that the attacker is doing XSS to steal user's cookie, hence the attacker COULD be
reflected the cookie back him. 
```

> 5TH QUESTION --> ANS: `26/04/2023 10:53:12`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/116de872-072d-4659-a383-eafacd29f4d2)

13. To find the UTC time, I started by analyzing the access.log file but did not find any supporting evidence.
14. Hence, I started to analyze the **phpbb_log** table and found a column named **log_operation** which indicates a successful login attempt for admin role.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d1621ffb-178d-4f0d-b1f8-0bb85f4ca3a2)


> RESULT 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7213dad3-6d11-4b7f-a30a-35fe7d078135)


> 6TH QUESTION --> ANS: Passw0rd1

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b59a15a0-ba49-44d2-bc2d-5f49f4f71bfd)


15. To get the password name, I just strings the database and grep for "ldap".

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7f344630-e013-4f17-8091-55470eff4317)


> 7TH QUESTION --> ANS: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/aec8b3ad-ea6b-41e3-b2f4-81d571b01eb4)


16. Simply check the user agent for ip --> `10.255.254.2` because we already identified before that the IP is Forela's.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3e322b9e-a855-48a5-acce-639cd971d2a2)


> 8TH QUESTION --> ANS: `26/04/2023 10:53:51`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c617074b-b8a4-47b9-9084-c6d2fbd0a35b)


17. Again, we need to check **LOG OPERATION** to get the time.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ad5dd7ca-be56-48c2-9020-20882d10bdda)


18. As you can see, after the attacker successfully logged in as admin, he began to add his own user account as part of the **admin** group.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/76a2582e-be4c-43c2-ab72-3dd570ef70b7)


19. To identify the timestamp, simply convert the epoch time to UTC.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9df2f862-bae6-487f-8189-176ffd8bfae1)



> 9TH QUESTION --> ANS: `26/04/2023 11:01:38`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/91f99521-2df8-455d-8838-cd26619e6331)


20. This time, I found the evidence when reviewing the access.log file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/79ed6a59-1f5c-4724-ae85-b691119fd81d)


21. Previously at table **phpbb_log** we can identify that the attacker attempted to do DB backup, then the timestamp is added at the backup's filename.
22. At this point, we are **VERY** sure this is the backup file.
23. Based from this log's line, we can see a **GET** request is made, the attacker tried to download the backup file the system previously created.
24. To get the UTC timestamp, simply substract 12 by 1 because the log's timestamp is +1.

> 10TH QUESTION --> ANS: 34707

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a37aa44c-0402-432d-98c1-8235427a2d2f)


25. Besides the status code, we can see the bytes or lengths for current request.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/218e2bd8-ccb6-4d07-bdb1-c732f9b2f766)


## IMPORTANT LINKS

```
https://sqliteviewer.app/
https://www.epochconverter.com/
```
