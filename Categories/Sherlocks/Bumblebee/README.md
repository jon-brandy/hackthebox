# Bumblebee
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cff2ee5e-4bfa-4d5b-90e3-a45e4e3516bb)

## Lesson learned:
- Accessing sqlite3 file.

## DESCRIPTION:
An external contractor has accessed the internal forum here at Forela via the Guest WiFi and they appear to have stolen credentials for the administrative user! 
We have attached some logs from the forum and a full database dump in sqlite3 format to help you in your investigation.

## STEPS:
1. In this challenge, we're given 2 files. A log file and a sqlite3 file.

> 1ST QUESTION --> ANS: 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e9d36caf-e15b-4127-ab16-45c2075aec86)


2. To get the username of the external contractor, we can start by accessing the sqlite3 database dump.
3. I start by execute query --> `SELECT name FROM sqlite_master WHERE type='table';`, which resulting to a few results. But one table_name caught should be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3270e1cc-a16a-43ff-ac92-63564c0d6bc4)


4. Execute this query --> `SELECT * FROM phpbb_users;` to check all columns and it's value.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c75ad478-c168-40be-9e7a-7e2258567a1a)


5. Noticed, there's a username with contractor mail.
6. 
