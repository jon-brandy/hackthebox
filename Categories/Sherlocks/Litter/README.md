# Litter
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1ad68f2c-9176-4546-8041-caa76fc3291e)


## Lesson learned:
- 

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




