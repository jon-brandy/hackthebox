# OpTinselTrace-4
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cd8145d8-6b54-4666-863f-bc092c1d0107)


## Lessons Learned:
- Hunt potential attacker's IP.
- Identify port scanning attempts.

## SCENARIO:
Printers are important in Santa’s workshops, but we haven’t really tried to secure them! The Grinch and his team of elite hackers may try 
and use this against us! Please investigate using the packet capture provided! The printer server IP Address is 192.168.68.128.

## STEPS:
1. In this challenge, we're given a packet capture of printer activities for IP 192.168.68.128.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/035ef3fd-f642-4c6e-b9e2-3a97c7cf1966)


> 1ST QUESTION --> ANS: `172.17.79.132`

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/16cfba6f-2c99-4872-91d1-15548b34f8a0)

2. To identify which IP address has an excessive amount of traffic to the printer server, we can check by go to **statistics -> IPv4 Statistics -> All Addresses**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/713b1f0f-dc2a-4caa-a68e-dc4272022725)

3. Based from the results above, we can identified 2 IPs with the most activities.
4. We can conclude that IP --> `172.17.79.132` is the answer.

> 2ND QUESTION --> ANS: 9100

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c4ec124b-053d-4c3a-b97a-843e78ddc419)

5. Next, to identify which port was then targeted for initial compromise of the printer, we can start by filter the source ip and analyze for port scanning attempts.
6. Based from the description, the printer's IP is `192.168.68.128`. Let's start by filter the IP.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/30ffb823-9c5c-47b7-9c3f-e680c914208f)


7. Based from the results above, we found several traffic with SYN flag and the packet bytes are small + request timestamp is very close in milisecond.
8. From this evidence, we can conclude the attacker attempted an nmap scans and we start analyzing these packets.
9. Scrolling down, we found several **ACK** response from the nmap scan for port **9100**. 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/15cd5e4e-d18b-44a9-93f8-fa60d65dc059)


10. Searching on the internet about default port for service printing, turns out that **9100** is the default port.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c254d742-e658-4b34-8ada-2c7b7ffb1593)


11. It's clear then, that port 9100 is the port exploited by the attacker. Not only that we identified that the attacker might be using 2 machine within NAT network remembering the IP used for scanning is --> `172.17.79.133`.

> 3RD QUESTION --> ANS: 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1e74f3e6-bd7f-46f8-ad2c-2487a2ffac77)


12. Following the packets to check 


> 4TH QUESTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3c0d8aa5-43a9-455e-b2c2-ac75f94db1c8)


> 5TH QUESTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/22536e2a-5675-4772-8cd5-3ba27b644dc3)


> 6TH QUESTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6eb586cf-48ff-4760-9bc1-8a6529dc8bd6)


> 7TH QUESTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e8f9d562-2d97-423c-b34f-3715909bfaf1)


> 8TH QUESTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/50741df6-93e9-4250-9f2c-18ed020f2322)


> 9TH QUESTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3ba31448-eed5-4d04-b57f-1c25cb03630d)


> 10TH QUESTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/65cd484d-7e77-44a2-8a0d-a3d5321596c6)


