# Bumblebee
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cff2ee5e-4bfa-4d5b-90e3-a45e4e3516bb)

## Lesson learned:
- Analyzing sqlite3 file.

## DESCRIPTION:
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


> 4TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e33d8301-d2d9-4a0f-b0ca-771ed0325659)


> 8TH QUESTION --> ANS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c617074b-b8a4-47b9-9084-c6d2fbd0a35b)



> 9TH QUESTION --> ANS: `26/04/2023 11:01:38`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/91f99521-2df8-455d-8838-cd26619e6331)


> 10TH QUESTION --> ANS: 34707

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a37aa44c-0402-432d-98c1-8235427a2d2f)


## IMPORTANT LINKS

```
https://sqliteviewer.app/
```
