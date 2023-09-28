# Arctic
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b8def82c-a07e-4cb3-8754-4b79732a46fb)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.11 --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-27 21:26 PDT
Stats: 0:01:38 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 78.74% done; ETC: 21:29 (0:00:26 remaining)
Nmap scan report for 10.10.10.11
Host is up (0.030s latency).
Not shown: 65532 filtered tcp ports (no-response)
PORT      STATE SERVICE VERSION
135/tcp   open  msrpc   Microsoft Windows RPC
8500/tcp  open  fmtp?
49154/tcp open  msrpc   Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 256.03 seconds
```

1. Based from the nmap results, the machine runs `Windows Remote Procedure Call (RPC)` and an unknown service at port 8500.
2. Interesting! Let's 
