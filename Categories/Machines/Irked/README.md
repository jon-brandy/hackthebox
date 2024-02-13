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
10. Also we need to set the remote host manually.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/28b87d95-1a4b-4eb7-9017-c1b1210f6d4d)


11. But it seems we need to specify the payload.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/626404d2-7e67-42f2-aee0-eb4d23ffc6b0)


12. Let's list all the available payloads.

## IMPORTANT LINKS

```
https://github.com/Ranger11Danger/UnrealIRCd-3.2.8.1-Backdoor
https://www.exploit-db.com/exploits/16922
```




