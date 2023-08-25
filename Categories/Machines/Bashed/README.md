# Bashed

> Write-up author: jon-brandy
 
## STEPS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/06d890ab-a95a-4c82-bc6f-c774d0792714)

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.68 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-25 02:31 PDT
Stats: 0:00:13 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 0.00% done
Nmap scan report for 10.10.10.68
Host is up (0.019s latency).
Not shown: 65534 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Arrexel's Development Site

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.82 seconds
```

1. Based from the result, the machine is running a web application.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bda28df5-de80-4de6-aff5-d6e891c3015e)


2. Found an interesting directory --> `/dev` which leads to a file named `phpbash.php`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/29cabec6-e47c-4ed4-90d5-fd801b6dd53d)

 
3. Why it's interesting, because the webpage documented about it, and based from the documentation it gives us a shell.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/02196f2f-b47e-4490-8a0a-275115c0bb24)


> GITHUB DOCUMENTATION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c7329fd1-1c43-40c2-8020-5c5ced9658f6)


4. So, opening the phpbash.php file will give us a shell.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/37acbeb0-1408-4712-8884-e985d34e4f54)


> GETTING USER FLAG

```
www-data@bashed
:/home# cd arrexel

www-data@bashed
:/home/arrexel# ls

user.txt
www-data@bashed
:/home/arrexel# cat user.txt

9d72b1d760c30a335315b4c35a83d8f5
```

## USER FLAG

```
9d72b1d760c30a335315b4c35a83d8f5
```

5. To get the root flag, obviously we need to do privesc.
6. Let's see are there any sudo permissions for `www-data`.

> RESULT

```
www-data@bashed
:/home/arrexel# sudo -l

Matching Defaults entries for www-data on bashed:
env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on bashed:
(scriptmanager : scriptmanager) NOPASSWD: ALL
```

7. Interesting, we can run any command as scriptmanager.
8. 
