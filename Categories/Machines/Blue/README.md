# Blue
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, let's scan the host given using nmap.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210322854-77ec16ab-4088-489e-a183-e97465f3e6d3.png)


![image](https://user-images.githubusercontent.com/70703371/210322875-26db3393-fc84-4860-85d0-21665f996a17.png)


2. Based from the output, we know that port 445 shall be our interests, because it seems running some types of network shares. Remember that 445 is SMB port, so let's check nmap scripts about `smb-vuln`.
3. Simply run this command:

```
ls /usr/share/nmap/scripts | grep smb-vuln
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210324250-9bb9a052-f634-48e8-b94c-ddf2b4b3dafb.png)


4. 
