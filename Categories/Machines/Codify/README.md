# Codify
> Write-up author: jon-brandy | Lesson learned: vm2 exploitations, 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ed060495-9bbf-4521-8586-e52f9f08aa52)

> PORT SCANNNING:

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.239 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-18 00:36 PST
Warning: 10.10.11.239 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.10.11.239
Host is up (0.033s latency).
Not shown: 53951 closed tcp ports (conn-refused), 11581 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 96071cc6773e07a0cc6f2419744d570b (ECDSA)
|_  256 0ba4c0cfe23b95aef6f5df7d0c88d6ce (ED25519)
80/tcp   open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://codify.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
3000/tcp open  http    Node.js Express framework
|_http-title: Codify
Service Info: Host: codify.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 275.72 seconds
```

1. Based from the nmap results, we can identified that the machine runs a web application, opens ssh login and using node.js framework for the webapp.

> WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/95dde7ef-9cee-480e-b93f-0a705d53d68d)


2. Reading the **About Us** page, shows us the door to exploit this web app, the `vm2 (virtual machine 2)` vuln.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/31abcec5-c414-408a-b0eb-170397adf10b)


3. Searching on the internet about vm2 vulns, shall resulting to this:

```
VM2 --> Is a library that provides a secure and sandboxed environment for executing JavaScript code. Primarily used in server side
environments such as Node-JS.

https://www.uptycs.com/blog/exploitable-vm2-vulnerabilities (the newest one --> 2023).
```

4. 
