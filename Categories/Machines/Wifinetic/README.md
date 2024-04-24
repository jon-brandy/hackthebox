# Wifinetic
> Write-up author: scorch

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/fe6395db-e99e-4b31-863b-30c3131d07cb)


## Lessons Learned:
- FTP Anonymous Login (information disclosure).
- Enumerating Wireless Network Interfaces.
- Identifying which network interface used as Access Point (BSSID) and which one is used as the WIFI Client.
- Dump Detailed each of Wireless Network Configurations (identified misconfig).
- Bruteforce WPS PIN using reaver (gained root access to the actual WIFI, because we could also get the PSK).

## STEPS:
> PORT SCANNING

```
┌──(scorch㉿getsleep)-[~/Downloads]
└─$ nmap -p- -sV -sC wifinetic.htb --min-rate 1000
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-04-23 22:41 PDT
Nmap scan report for wifinetic.htb (10.10.11.247)
Host is up (0.029s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT   STATE SERVICE    VERSION
21/tcp open  ftp        vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 ftp      ftp          4434 Jul 31  2023 MigrateOpenWrt.txt
| -rw-r--r--    1 ftp      ftp       2501210 Jul 31  2023 ProjectGreatMigration.pdf
| -rw-r--r--    1 ftp      ftp         60857 Jul 31  2023 ProjectOpenWRT.pdf
| -rw-r--r--    1 ftp      ftp         40960 Sep 11  2023 backup-OpenWrt-2023-07-26.tar
|_-rw-r--r--    1 ftp      ftp         52946 Jul 31  2023 employees_wellness.pdf
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.8
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
53/tcp open  tcpwrapped
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.50 seconds
```

1. Based from the nmap results, the machine opens FTP service, ssh service, and it's unclear what service is running at port 53. But based on it's port number, most likely it acts as a DNS Server.
2. Noticed we can login using anonymous user in FTP.

> LOGIN USING ANONYMOUS USER

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/ad250528-b56f-4844-af97-7101be0d0870)


3. Found few files there! Let's download eadh files from current FTP directory to our local machine.
4. Upon reviewing each files, .tar file contained configuration files along with users registered on the machine.

> Dirs and files inside the .tar file

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/03b1e129-ac25-4674-bddb-36201827ddf8)

5. Reviewing the `passwd`, found a normal user (netadmin).

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/08c0f3d2-1c10-4a48-9f14-8e7d82c0c553)


6. Interestingly, there is no `shadow` file. So we can't crack hashes, the approach seems to identify any disclosed information or any weak configurations.
7. Long story short, upon traversing and reviewing each files, found one file which disclosed a password.

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/b83c7bf3-4e29-468c-9693-0ce567bae41c)


8. I'm speculating it's the cred for `netadmin` user, let's try it.

> We authenticated and got the user flag.

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/5772911e-fd16-4f8b-884c-17a77995be0a)


## USER FLAG

```
554891fe4881530f6ddd7ce52602c8a4
```

9. Nice! Now the point for wifi exploitation is to gained the password to the actual wifi (accessing root means we're accessing the actual client wifi).
10. Now let's enumerating wireless network interfaces and identify which interface acts as the **Access Point (AP)** and which interface acts as the **Client Wifi**.

> ifconfig

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/29b32b91-59b9-4be8-9a50-843f9b187996)


11. Found 3 wireless network interfaces, but only 2 that seems to be our interest (both assigned with IP address).
12. However, another network interface seems to be our interest at the future.

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/57e5f18f-4d93-4b0b-90fb-d373723dcd89)


#### NOTES:

```
mon0 interface is a monitor mode, this interface commonly used for wireless network monitoring. Also it
can be used for testing purposes (which also can be used for bruteforcing the WPS PIN).
```

13. Interesting, now we can focus on `wlan1`, `wlan0`, and `mon0`.
14. Now let's identify which interface acts as AP and which acts as the Client Wifi.

> Execute --> iw config

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/c06ae2bf-8557-410f-8ea3-a220a06eb9d6)

 
15. But again, to make sure our understanding we can check the `hostapd` and `wpa_supplicant` files.

> RESULT FOR BOTH FILES

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/48a108c5-ef75-48ac-9ee6-32d400691d7f)


16. Awesome now we found our target, let's bruteforce the WPS PIN of WLAN1.
17. Tool used to bruteforce the PIN, is using `reaver`. To identify whether the machine has reaver, simply execute the basic bins enumeration --> `getcap -r / 2>/dev/null`.

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/0d3bc332-6687-4634-9d97-cb49a4243718)


18. Found it. To bruteforce the WPS PIN, we need to identify the BSSID or AP of WLAN1.
19. To identify it, we can using `iwconfig`.

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/a94d3f04-d1d5-4303-b4d0-ebda1d6aed96)


20. Now, remembering there is `mon0` interface, we can use it to perform the WPS PIN Attack because that interface is used to capture WPS handshake packets exchanged during the WPS PIN authentication process.
21. To perform it, we also use `reaver` to leverage captured WPS handshake packets to perform offline brute-force attacks against the WPS PIN. This can be done by repeatedly attempting different PIN combinations.

#### NOTES:

```
Monitorin interfaces, such as mon0 can also be used for passive sniffing of WI-FI traffic
without associating with specific network.

Knowing this, the attackers are allowed to capture and analyze Wi-Fi frames, including
those related to the WPS negotiation.
```

22. Another tricky part, to use `reaver` we also need to identify the channel number of the frequency.
23. To identify it simly open the wikipedia for each frequencies's channel.
24. Since our target has frequency of `2.412` GHz, hence the channel number is 1.

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/42ffd903-730c-4712-94e5-97105998066e)


![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/bbf8ae75-0c7b-4542-ad57-6ee24e548d42)


> Reaver Command

```
reaver -i mon0 -c 1 -vv -b 02:00:00:00:00:00
```

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/64e5d4e4-0829-4c9d-981d-7ce3f94fc15f)


25. Awesome we got the PIN and also we got the PSK password.

![gambar](https://github.com/jon-brandy/hackthebox/assets/70703371/2e29d9e3-4f23-49f0-aab0-98a3885860f3)




## IMPORTANT LINKS / NOTES

For more detailed info about the network configurations, execute `iw dev`.

```
netadmin@wifinetic:~$ iw dev
phy#2
        Interface mon0
                ifindex 7
                wdev 0x200000002
                addr 02:00:00:00:02:00
                type monitor
                txpower 20.00 dBm
        Interface wlan2
                ifindex 5
                wdev 0x200000001
                addr 02:00:00:00:02:00
                type managed
                txpower 20.00 dBm
phy#1
        Unnamed/non-netdev interface
                wdev 0x1000000e9
                addr 42:00:00:00:01:00
                type P2P-device
                txpower 20.00 dBm
        Interface wlan1
                ifindex 4
                wdev 0x100000001
                addr 02:00:00:00:01:00
                ssid OpenWrt
                type managed
                channel 1 (2412 MHz), width: 20 MHz (no HT), center1: 2412 MHz
                txpower 20.00 dBm
phy#0
        Interface wlan0
                ifindex 3
                wdev 0x1
                addr 02:00:00:00:00:00
                ssid OpenWrt
                type AP
                channel 1 (2412 MHz), width: 20 MHz (no HT), center1: 2412 MHz
                txpower 20.00 dBm
```

```
https://outpost24.com/blog/wps-cracking-with-reaver/
```

