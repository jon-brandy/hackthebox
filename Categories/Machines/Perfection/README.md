# Perfection
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a25ccf1b-8041-48e5-9d09-020a945528ef)


## Lessons Learned:
- Exploiting WEBrick 1.7.0

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC 10.10.11.253 --min-rate 1000                                           
Starting Nmap 7.93 ( https://nmap.org ) at 2024-03-17 20:39 PDT
Nmap scan report for perfection.htb (10.10.11.253)
Host is up (0.017s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 80e479e85928df952dad574a4604ea70 (ECDSA)
|_  256 e9ea0c1d8613ed95a9d00bc822e4cfe9 (ED25519)
80/tcp open  http    nginx
|_http-title: Weighted Grade Calculator
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.77 seconds
```

1. Based from the nmap results above, the machine runs a web application at port 80 and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/aa0e65bb-d7f4-4cef-ac2a-6f97fb41f177)


2. Scrolling down to the footer section, we identified the web server used is **WEBrick** which is a RUBY library.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/deb7b11b-a64a-47b2-a6b1-44b2819fb424)


3. Searching on the internet about vulns found in **WEBrick 1.7.0** resulting to none.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/29519086-e07e-46de-aae0-af2cfb55c438)


4. Scanning for subdomain and directories also resulting to none. However our interest should be at the **weight grade calculation** feature.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5e3e3123-8c34-4a6d-995e-0ecffda31a1c)


5. After sent normal input, seems it just calculate our grades normally. Nothing special at client-side.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2f3a453e-a418-47a1-90b7-9cff9ec31e83)


6. Tried to execute client-side attack, the webapp reflects us **Malicious Input Blocked**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/26e43bd2-e5a9-4a3a-8cf6-8e90ffccc596)


7. Let's use repeater for further testing.
8. The reflect message is caused because I input the malicious script/code at the **category** column.
9. This time I tried to send `;id ` but encode it with URL.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/48782621-d8df-40c9-bce7-ecac7e8ee39c)


10. It's still blocked.
11. Let's try to send URL encoded newline (\n) to test whether
 


## IMPORTANT LINKS

```
https://security.snyk.io/package/rubygems/webrick
https://portswigger.net/kb/issues/00100f00_ruby-code-injection
```
