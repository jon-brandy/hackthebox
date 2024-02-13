# Irked
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b829affd-39fa-473d-9d82-2270d552f7af)


## Lessons Learned:
1. Unreal3.2.8.1 is vulnerable to backdoor command execution.
2. Exploiting irc service for version Unreal3.2.8.1 using metaploit.

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.117 --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2024-02-13 05:14 PST
Nmap scan report for irked.htb (10.10.10.117)
Host is up (0.19s latency).
Not shown: 65528 closed tcp ports (conn-refused)
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
| ssh-hostkey: 
|   1024 6a5df5bdcf8378b675319bdc79c5fdad (DSA)
|   2048 752e66bfb93cccf77e848a8bf0810233 (RSA)
|   256 c8a3a25e349ac49b9053f750bfea253b (ECDSA)
|_  256 8d1b43c7d01a4c05cf82edc10163a20c (ED25519)
80/tcp    open  http    Apache httpd 2.4.10 ((Debian))
|_http-title: Site doesn't have a title (text/html).
111/tcp   open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          47638/udp6  status
|   100024  1          53595/tcp6  status
|   100024  1          55178/udp   status
|_  100024  1          55862/tcp   status
6697/tcp  open  irc     UnrealIRCd
8067/tcp  open  irc     UnrealIRCd
55862/tcp open  status  1 (RPC #100024)
65534/tcp open  irc     UnrealIRCd
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 107.56 seconds
```

1. Based from the nmap results, the machine runs several service.
2. Http on port 80, ssh on port 22, interestingly irc on few IPs, and rpcbind on port 111.

#### NOTES:

```
RPC (Remote Procedure Call) is a protocol that one program can use to request a service from a program located on another computer in a network.
```

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1162f22c-c5c2-4bab-b7f9-4d1ae8aca4af)


3. Interesting, seems our focus should be at the IRC service.
4. Now let's find the IRC's version by running **irssi** to any port that runs irc service.

```
irssi -c irked.htb --port 6697
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/17473e0f-a574-446b-b112-6acb46ae3224)


5. Great! Now we know the service version is --> `Unreal3.2.8.1`.
6. Searching on the internet about vuln for the related version found several results which leads to this.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/52092b8a-8c95-4e97-a3e7-86dda5451ce2)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8e5e4570-24d1-486d-8a5c-297f6b328cf4)


7. It seems the service is vulnerable to **backdoor command execution**.
8. Let's search the module in metasploit.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/73f4fb71-d6d3-4d2b-b4fe-a2dbe38cf752)


9. It seems the remote port is already set to 6667 and we need to re-set it to one of the port which runs the irc service in our remote host.
10. Also we need to set the remote host, local host, and local port manually.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/28b87d95-1a4b-4eb7-9017-c1b1210f6d4d)


11. But it seems we need to specify the payload.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/626404d2-7e67-42f2-aee0-eb4d23ffc6b0)


12. Let's list all the available payloads.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/965d7e85-d3ba-4303-b2d0-4e7cd2d2fe5b)


13. Payload number 6 seems promising.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4fba7d6b-1794-4c55-9e4a-d972f9cbd9f8)


> RUN IT AGAIN.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5808df47-d4e4-4a11-8a0c-b807054797bc)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ad27c69-b72a-439e-8907-9aef23a1a1e3)


14. Great we got a shell.

> GETTING THE USER FLAG


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3e51d566-0f8a-4931-bf36-aecbf555aadd)



![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c0bd3715-5c1c-409f-8c47-91d6b5181eed)


15. It seems we don't have the permission to access the user.txt file because it's created by root user, hence we need to gained root in order to see the contents.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f844b38f-ffbd-416a-810d-a83ecb432e3b)


16. But noticed there's a hidden file named `.backup`.
17. Based from the content, it should be related to **steghide** usage.
18. However, we need to find the correct file which should be the target now.
19. Remembering at the homepage of the webapp, it shows an image which states the hint for us to exploit the irc service.
20. Let's use **steghide** to that image. The image itself can be found inside `/var/www/html`.
21. Sadly the remote host does not have steghide, let's exfiltrate the image file to our localhost by setting up the python server at the remote host and run **wget** at our localhost.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bcda066f-1fd6-4860-bfb9-6a11b4c523cf)


> RESULT


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/33b9dafc-97a8-4098-8f69-7cebd2c9941a)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fdbfc665-4f25-48af-983b-998e1fb59d23)


22. Turns out it's the password, so user **djmardov** stored a backup password at his own home directory.

> AUTH AS DJMARDOV


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f72be77a-b650-4477-9fc7-71fa3db6697c)


> GETTING USER FLAG


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c4dc16e4-f95e-448e-85a9-84d2bea7e8ae)


## USER FLAG

```
7c7bc374daaf4d94fff0b6259eb7446d
```


## IMPORTANT LINKS

```
https://github.com/Ranger11Danger/UnrealIRCd-3.2.8.1-Backdoor
https://www.exploit-db.com/exploits/16922
```




