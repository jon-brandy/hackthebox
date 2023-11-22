# Meerkat
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c8f0ae29-0794-4aa0-b872-8ee11b1ce17e)


## DESCRIPTION:
As a fast growing startup, Forela have been utilising a business management platform. 
Unfortunately our documentation is scarce and our administrators aren't the most security aware. 
As our new security provider we'd like you to take a look at some PCAP and log data we have exported to confirm if we have (or have not) been compromised.

## HINT:
- NONE
## STEPS:
1. In this challenge we're given two files.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/317a7617-95f3-4020-8255-a3676d20bec2)


> 1ST QUESTION --> ANS : Bonitasoft

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/633d94c8-2997-4a84-9322-8728099a8d4d)


2. To answer it, I started by analyzing the .pcap file.
3. Found out that there are several request with POST method to `172.31.6.44`. The endpoint is `/bonita/loginservice`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58833602-a454-4e6b-a30c-6c97080f7369)


5. Searching for **Bonita** at the .json file, shall resulting to `Bonitasoft`. Great now we know the ans is `Bonitasoft`.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3034bbfd-bbfc-4212-9836-1b942ef56356)
