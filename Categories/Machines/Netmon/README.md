# Netmon
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, scan all open ports and it's service from the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210515351-571921b4-c807-48c8-81ba-b66341c4f851.png)


![image](https://user-images.githubusercontent.com/70703371/210515384-542e5a38-cdd1-4470-8fce-e857126c91c2.png)


![image](https://user-images.githubusercontent.com/70703371/210515422-c2275f3f-a477-4d4c-994b-58e871ac2e57.png)


2. Based from the result here, we know that **anonymous ftp login allowed** and the machine seems running a web service at port 5985. Not only that there's **SMB** ports open.
3. And it seems there's a vuln with the smb service.

![image](https://user-images.githubusercontent.com/70703371/210516180-3cea3746-0091-4e05-b99e-f0b6d0e8837c.png)

4. Anyway let's login with ftp.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210516407-cb5ee042-3e12-40a1-8aaf-d309e88e84ff.png)


![image](https://user-images.githubusercontent.com/70703371/210516445-6ec237bd-8550-4dc1-823c-81ad8e10a855.png)


