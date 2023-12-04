# Litter
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1ad68f2c-9176-4546-8041-caa76fc3291e)


## Lesson learned:
- DNS tunneling.

## DESCRIPTION:

Khalid has just logged onto a host that he and his team use as a testing host for many different purposes, it’s off their corporate network but has access to lots of resources in network. The host is used as a dumping ground for a lot of people at the company but it’s very useful, so no one has raised any issues. Little does Khalid know; the machine has been compromised and company information that should not have been on there has now been stolen – it’s up to you to figure out what has happened and what data has been taken.

## STEPS:
1. In this challenge we're given a .pcap file.

> WIRESHARK

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5f0a5001-686f-4c28-889a-6bfd67fe288f)


> 1ST QUESTION --> ANS: DNS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a37d9ce5-cbf7-47b5-a1ec-19638c38e847)

2. Analyzing the packets, it is known that most of the hostname is a large number of hexadecimals.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/de16fb07-8a1c-4ada-89e7-a241aa714ffa)


3. This pattern is referring to `DNS tunneling` technique, hence we can conclude the malicious protocol is DNS.


> 2ND QUESTION --> ANS: 192.168.157.145

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cd4debd8-3524-4adf-9c65-fe7d42c898f9)


4. Based from the previous malicious traffic we found, we can conclude the suspected host is --> `192.168.157.145`.

> 3RD QUESTION --> ANS: whoami

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6aa035e6-25fb-4a7b-9889-ef3cce8b522c)


5. Following one of the UDP packet streams and decode it with cyberchef, shall let us find the first command the attackers sends to the client.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8451a2f1-6a89-41d8-9b8c-a1da9e77d704)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/734c4c4e-4f87-4e00-ac5c-aa675daf4865)


> 4TH QUESTION --> ANS: 0.07

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e7eabc66-c4fc-4b4e-b856-c6cd7e337533)


6. To identify the version of DNS tunneling tool used, simply analyze the previous decoded hex.
7. Scrolling down, we shall find the version.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3d087d8e-ca8c-48b2-b1fa-7d1e8680547e)


> 5TH QUESTION --> ANS: win_install.exe

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9d221578-a496-42f5-9b2a-685fae232ec9)


8. Based from the previous question, we can assume that the attacker accidentally left the dns tool not renamed.
9. Hence, I scrolling down again and searched for a renaming command and found this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4fced9bf-d34c-4b7b-8d3c-6d34447959ca)


10. As you can see, the attacker tried to use `ren` command which is a shorthand of `rename` in windows command.

> 6TH QUESTION --> ANS: 0 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2b891f42-ba2f-4959-80c8-442b066eb070)


11. The users cloud storage is at `OneDrive`, scrolling down the decoded packet stream shall found out that there is no files inside it.
12. Hence, we can conclude the attacker did not locate any file in the user cloud storage.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a6fe52a4-29dd-49d7-9985-722b6b86b0b4)


> 7TH QUESTION --> ANS: C:\users\test\documents\client data optimisation\user details.csv

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1bbef92a-0060-4c07-a681-ec221a433fc5)


13. Again, scrolling down the same decoded packet stream, shall found the full path of PII file which is stolen.
14. Actually I found few `.csv` file which is interesting but only one so far that the attacker attempted to read.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6c685d8e-dcb1-4591-a1f4-df9b52287c4c)


15. Scrolling down again, you shall find the attacker indeed have an interest in this file and attempted to download it.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df82bee2-0e20-4a0b-9c20-ac641c71699e)



> 8TH QUESTION --> ANS: 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/df13f87a-2057-45de-9368-36ba257d8d76)


16. To identify how many PII records were stolen, I download the cyberchef results and count manually there.
17. Took me a very long time to analyze it, maybe there's an intended way to solve it.
18. However, found out the amount of PII stolen is 721.

## IMPORTANT LINKS:

```
https://www.socinvestigation.com/how-dns-tunneling-works-detection-response/
```
