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
8. For volatility i'm using **SIFT** but somehow the custom profile does not listed there.
9. So i tried to use volatility in Kali and successfully stored the custom profile. Path -> `/volatility/volatility/plugins/overlays/linux`.
10. To check whether it stored or not simply run -> `python2 vol.py --info`.

![image](https://user-images.githubusercontent.com/70703371/233845191-0041e2bb-2d2e-411a-bc5b-a2f105efd9da.png)


11. With this, we don't need to run **imageinfo** to find the correct profile.
12. Let's run **pslist** to then.

```console
┌──(vreshco㉿nic)-[~/Downloads/htb_retired]
└─$ python2 ../../../../opt/volatility/vol.py -f mem.dmp --profile=LinuxUbuntu_4_15_0-184-generic_profilex64 linux_pslist
```

![image](https://user-images.githubusercontent.com/70703371/233845967-ce676504-bcbd-4ada-9bdc-c9b2f610b853.png)


13. Well it's still hard to guessing which processes is malicious.
14. Let's check all the bash commands used.

```console
┌──(vreshco㉿nic)-[~/Downloads/htb_retired]
└─$ python2 ../../../../opt/volatility/vol.py -f mem.dmp --profile=LinuxUbuntu_4_15_0-184-generic_profilex64 linux_bash
```

![image](https://user-images.githubusercontent.com/70703371/233846197-9222b664-c4c8-4b4b-b015-2d021701dced.png)


15. Seems like `./configure` is the correct ans (?)

![image](https://user-images.githubusercontent.com/70703371/233846248-ca278d23-c842-4878-9d48-953a32584c4d.png)


16. Now it's asking the md5sum of the ransomware file, to get that we can use **md5sum**.
17. Remembering the 1st question asked about the ransomware file link, hence we can grab the file by exporting the http packet from wireshark.

```
Export Objects -> HTTP
```

18. Extract the .tar file -> jump to the directory -> run md5sum.

![image](https://user-images.githubusercontent.com/70703371/233846621-b27702f7-e4c1-4dbe-b580-7d487061aae5.png)


19. We got it correct! Now it's asking the programming language used.
20. From the directory name it should be python, but when i run strings, i found syntaxes used in c, could be pyc (?) But C is just the extension of python, so we can say it's python.

![image](https://user-images.githubusercontent.com/70703371/233846853-7b3b7ffd-97d6-483a-b351-b551abd76c28.png)


21. Got it correct! Now it's asking the function name used for encryption.
22. Let's decompile the binary, since the binary is stripped, it's harder for us to identify the function name.
23. But things to know, it's a python c binary file, hence we can't use ghidra to decompile it.
24. I did a small outsource about this, until i found [this](https://github.com/extremecoders-re/pyinstxtractor) tool to decompile python binary file.
25. Tried **decompyle3** but somehow it won't work for me, so i used this tool.

![image](https://user-images.githubusercontent.com/70703371/233848581-23855620-a387-4175-9550-bd7482515f1d.png)


26. Open the extracted directory, our interest is at the configure.pyc file, we need to decompile that to py.









