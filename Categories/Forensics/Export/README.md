# Export
> Write-up author: jon-brandy
## DESCRIPTION:
We spotted a suspicious connection to one of our servers, and immediately took a memory dump. Can you figure out what the attackers were up to?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211019893-b78c82e1-70bb-413a-b314-f18a6f6f78f5.png)


2. Got a `.raw` file which is a memory dump of a system in which memory forensics was done to figure out what is going on during the time the dump created.
3. So let's use memory forensics tools named Volatility.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211020582-d07bc4fb-2d3f-4cd1-a0b3-c6abcb18af6c.png)


4. Based from the result, the top suggested profile is `Win7SP1x64` which means that the system in question is likely a Windows 7 SP1 64 bit system.
5. Since the profile is determined, hence we can run this command:

```
vol.py -f WIN-LQS146OE2S1-20201027-142607.raw --profile=Win7SP1x64 pslistt
```

> RESULT


![image](https://user-images.githubusercontent.com/70703371/211022014-aff558f1-0529-47ab-8c1d-439166cd9117.png)


6. The `cmd.exe` caught my attention, let's use `cmdscan`.


```
vol.py -f WIN-LQS146OE2S1-20201027-142607.raw --profile=Win7SP1x64 cmdscan
```


> RESULT


![image](https://user-images.githubusercontent.com/70703371/211022509-2f688e88-9539-4bac-b993-360d651beb6e.png)



7. Let's paste the encoded url to cyberchef.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211022633-db4df89a-8ed4-44a4-a745-e514406b8d8a.png)


8. Notice there's a base64 encoded text.

![image](https://user-images.githubusercontent.com/70703371/211022705-f0a59c53-d13d-464c-819e-9555844beca1.png)


10. Let's decode that.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211022870-50bce364-6b91-4937-928d-5a0c44966c80.png)


11. Got the flag!

## FLAG

```
HTB{W1Nd0ws_f0r3Ns1CS_3H?}
```

