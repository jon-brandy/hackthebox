# POOF
> Write-up author: vreshco
## DESCRIPTION:
In my company, we are developing a new python game for Halloween. I'm the leader of this project; thus, I want it to be unique. 
So I researched the most cutting-edge python libraries for game development until I stumbled upon a private game-dev discord server. 
One member suggested I try a new python library that provides enhanced game development capabilities. 
I was excited about it until I tried it. Quite simply, all my files are encrypted now. 
Thankfully I manage to capture the memory and the network traffic of my Linux server during the incident. 
Can you analyze it and help me recover my files? To get the flag, connect to the docker service and answer the questions.
## HINT:
- NONE
## STEPS:
1. Unzipping the files resulting to 4 files extracted.

![image](https://user-images.githubusercontent.com/70703371/233778441-19157ecd-0174-4e42-8871-cdc0a2992155.png)


2. Let's open the host.

![image](https://user-images.githubusercontent.com/70703371/233778521-4461599d-fcac-436a-91ba-e985392e955f.png)


3. It seems we need to find the malicious URL, remembering we have a .pcap file, obviously we can get it from there, let's analyze the HTTP packets.

![image](https://user-images.githubusercontent.com/70703371/233778603-89341ca0-0abd-47c6-bc54-d9a78368395d.png)


4. Looking at the request headers (host, path) we know the malicious URL where the ransomware downloaded from.

```
http://files.pypi-install.com/packages/a5/61/caf3af6d893b5cb8eae9a90a3054f370a92130863450e3299d742c7a65329d94/pygaming-dev-13.37.tar.gz
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/233778822-16dab4a0-7c14-4cab-adb3-1c16d5bc2a69.png)


5. Now it's asking what is the name of the malicious process, we can get the ans by analyzing the dump file using **volatility**.
6. Notice there's a `Ubuntu_4.15.0-184-generic_profile.zip`, by it's name obviously it's a profile.
7. Since we're given the profile in a .zip file, we need to move it to our volatility overlays directory, specifically in it's linux directory.
8. For volatility i'm using **SIFT**.

```console
sansforensics@siftworkstation: ~/Downloads/poof
$ sudo mv Ubuntu_4.15.0-184-generic_profile.zip ../../../../usr/local/lib/python2.7/dist-packages/volatility/plugins/overlays/linux/
```

9. 





