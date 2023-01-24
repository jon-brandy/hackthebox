# Strike Back
> Write-up author: jon-brandy
## DESCRIPTION:
A fleet of steam blimps waits the final signal from their commander in order to attack gogglestown kingdom. 
A recent cyber attack had us thinking if the enemy managed to discover our plans and prepare a counter-attack. Will the fleet get ambused???
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214206472-10e6c6df-228f-42b6-bb63-1f79dfb42ae3.png)


2. Check both file types.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214206750-07982c40-0f7b-4cd1-bfaf-cfec3e95dea5.png)

3. The `.dmp` files contains **Mini DuMP crash report, 17 streams**. Let's strings that file to see if we can get any clue.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214206934-6ccd5134-1714-408d-970c-8c653f346d95.png)


![image](https://user-images.githubusercontent.com/70703371/214206996-01294d22-cf52-4f89-bf4c-da039d30032e.png)


![image](https://user-images.githubusercontent.com/70703371/214207001-9600ef30-218c-41b3-b51d-0241e6700e7d.png)


4. Got a username -> `npatrick` and notice the user seems download a `PE` file named **freesteam.exe**. Let's binwalk the `.dmp` file, to see if there are any files we can extract.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214207262-c935a82d-c2ab-4034-9cc3-148cb434d5da.png)


> EXTRACTED

![image](https://user-images.githubusercontent.com/70703371/214207333-2635988e-3c01-4612-b98b-4952e227375c.png)


![image](https://user-images.githubusercontent.com/70703371/214207514-ec0b7d02-8d69-426e-a175-752af64f8772.png)



5. Hmm.. Let's open the `.pcap` file then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214207548-e638691a-49a5-4f7d-b8fc-f29fc8e6b51e.png)


6. All the http packets seems should be our interest here, let's export all of them.

![image](https://user-images.githubusercontent.com/70703371/214208502-179655dc-2b33-4d7f-b713-d1941079ff7b.png)


![image](https://user-images.githubusercontent.com/70703371/214208658-a36c769d-29f8-4a25-aecc-bc93428f7713.png)


![image](https://user-images.githubusercontent.com/70703371/214208926-ba03f716-c677-4ad2-a226-1211867fcc20.png)


7. Let's decompile the `freesteam.exe`.
8. When analyzing this function.

![image](https://user-images.githubusercontent.com/70703371/214209454-ce505c2e-1be2-4bb3-8a0f-cd3fb2a4c4a4.png)

> This undefined function seems execute a shellcode

![image](https://user-images.githubusercontent.com/70703371/214209588-fa5e494b-5327-4ecf-9eba-aa77eeac78bd.png)


9. Since it's a forensic challenge, i tried to upload the `PE` file to **virustotal** webapp and got this:

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214209878-7bf0608d-914c-4224-86a7-ea8e3f94da01.png)


![image](https://user-images.githubusercontent.com/70703371/214209907-4e2a4c2e-40f9-4495-949d-9967bc61e2dd.png)


10. Based on the output, i think this chall related to **Cobalt Strike Beacon Attacks**. I did a small outsource about this attack and found several article discussing this concept.

```
https://blog.nviso.eu/2021/10/21/cobalt-strike-using-known-private-keys-to-decrypt-traffic-part-1/
https://blog.nviso.eu/2021/11/17/cobalt-strike-decrypting-obfuscated-traffic-part-4/
https://blog.nviso.eu/2021/11/03/cobalt-strike-using-process-memory-to-decrypt-traffic-part-3/
https://blog.didierstevens.com/2021/10/11/update-1768-py-version-0-0-8/
```

11. First let's get the public and private key (if there is) using [this](https://blog.didierstevens.com/2021/10/11/update-1768-py-version-0-0-8/) python script.

```sh
python 1768.py ../../../Downloads/htb/foren/freesteam.dmp -V
```

> RESULT

```
File: ../../../Downloads/htb/foren/freesteam.dmp
Config found: xorkey b'.' 0x00000000 0x00010000
0x0001 payload type                     0x0001 0x0002 0 windows-beacon_http-reverse_http
0x0002 port                             0x0001 0x0002 80
0x0003 sleeptime                        0x0002 0x0004 60000
0x0004 maxgetsize                       0x0002 0x0004 1048576
0x0005 jitter                           0x0001 0x0002 0
0x0006 maxdns                           0x0001 0x0002 255
0x0007 publickey                        0x0003 0x0100 30819f300d06092a864886f70d010101050003818d003081890281810090675223e8a456ebda21cb31552d9f58e675bfa1dabeefbdc3071e5d8d9e263500f9665ce43bc9d0e51aa869b19250d855c8c19f3bac59fc7b4de2164ba4e9327f713436fb283d6cc7326b40755f39209643c1a13bcaaeef082b7a070342254cb2a971c17e43ec095a598678fd02360097fb4a3740d279c8ca61ed3e1b5de96d020301000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0x0008 server,get-uri                   0x0003 0x0100 '192.168.1.9,/match'
0x0009 useragent                        0x0003 0x0080 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET4.0C)'
0x000a post-uri                         0x0003 0x0040 '/submit.php'
0x000b Malleable_C2_Instructions        0x0003 0x0100 '\x00\x00\x00\x04'
0x000c http_get_header                  0x0003 0x0100
  Cookie
0x000d http_post_header                 0x0003 0x0100
  &Content-Type: application/octet-stream
  id
0x000e SpawnTo                          0x0003 0x0010 (NULL ...)
0x001d spawnto_x86                      0x0003 0x0040 '%windir%\\syswow64\\rundll32.exe'
0x001e spawnto_x64                      0x0003 0x0040 '%windir%\\sysnative\\rundll32.exe'
0x000f pipename                         0x0003 0x0080 (NULL ...)
0x001f CryptoScheme                     0x0001 0x0002 0
0x0013 DNS_Idle                         0x0002 0x0004 0 0.0.0.0
0x0014 DNS_Sleep                        0x0002 0x0004 0
0x001a get-verb                         0x0003 0x0010 'GET'
0x001b post-verb                        0x0003 0x0010 'POST'
0x001c HttpPostChunk                    0x0002 0x0004 0
0x0025 license-id                       0x0002 0x0004 16777216 Stats uniques -> ips/hostnames: 17 publickeys: 17
0x0026 bStageCleanup                    0x0001 0x0002 0
0x0027 bCFGCaution                      0x0001 0x0002 0
0x0036 HostHeader                       0x0003 0x0080 (NULL ...)
0x0032 UsesCookies                      0x0001 0x0002 1
0x0023 proxy_type                       0x0001 0x0002 2 IE settings
0x003a                                  0x0003 0x0080 '\x00\x04'
0x0039                                  0x0003 0x0080 '\x00\x04'
0x0037                                  0x0001 0x0002 0
0x0028 killdate                         0x0002 0x0004 0
0x0029 textSectionEnd                   0x0002 0x0004 0
0x002b process-inject-start-rwx         0x0001 0x0002 64 PAGE_EXECUTE_READWRITE
0x002c process-inject-use-rwx           0x0001 0x0002 64 PAGE_EXECUTE_READWRITE
0x002d process-inject-min_alloc         0x0002 0x0004 0
0x002e process-inject-transform-x86     0x0003 0x0100 (NULL ...)
0x002f process-inject-transform-x64     0x0003 0x0100 (NULL ...)
0x0035 process-inject-stub              0x0003 0x0010 'd\\ÃÂê·Íñ¡T,¬\x13¾\x0c\x07'
0x0033 process-inject-execute           0x0003 0x0080 '\x01\x02\x03\x04'
0x0034 process-inject-allocation-method 0x0001 0x0002 0
0x0000
Guessing Cobalt Strike version: 4.2 (max 0x003a)
```

12. Got the public key but no private key. Also there's `Malleable_C2_Instructions` -> `\x00\x00\x00\x04`.







