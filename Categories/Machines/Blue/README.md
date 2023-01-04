# Blue
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, let's scan the host given using nmap.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210548655-c761e148-c1bf-4b32-a17e-8c1a72c690fb.png)


![image](https://user-images.githubusercontent.com/70703371/210548679-5dd82615-0a4e-44e9-a4bf-2cd51961c46b.png)


2. Based from the output, we know that port 445 shall be our interests, because it seems running some types of network shares. Remember that 139 & 445 is SMB port, so let's check nmap scripts about `smb-vuln`.
3. Simply run this command:

```
ls /usr/share/nmap/scripts | grep smb-vuln
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210548775-11ed93fa-0149-40a9-920a-1257c94d9989.png)


4. Now let's use all of them for port 139 & 445.

```
nmap --script smb-vuln* -p 139,445 10.10.10.40
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210548814-20b88593-4861-4a8e-a675-e21edf35b868.png)


5. As we can see the vuln here is we can do RCE, also we got the link references:

![image](https://user-images.githubusercontent.com/70703371/210548936-bad60e4f-f1df-4909-83f4-d59a102c7e0e.png)


6. Anyway, i will try to use the **metasploit** first, then i'll try to solve it without metasploit.

### WITH METASPLOIT

1. First, open **msfconsole**, then input this command -> `search ms17-010`

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210549303-6f6bd9b9-3f1f-410c-b3af-6df4c444cee0.png)


2. The modules we want to use must be `0` , `2`, and `3`. But let's try with `0` and `2` first.

```
Reason:
The 1st module -> Is intended for windows 8, which is not the system.
The 3rd module -> Is auxiliary, though it says command execution, let's put is last. 
The 4th module -> Is a scanner.
The 5th module -> Is using a backdoor (must be on the system already).
```

3. Let's type `use 0`.

> RESULT - set the RHOSTS and lhost

![image](https://user-images.githubusercontent.com/70703371/210550559-ac898d76-deac-4ca8-8222-543969989a1d.png)

4. Type `exploit`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210550767-4e327376-f153-4d65-bfdf-3e1ffbb8dbcb.png)


![image](https://user-images.githubusercontent.com/70703371/210550828-15d51f7d-6a90-4a73-96f7-c55d5ab6a9d5.png)


5. Great! Turns out we're already the root.
6. Let's set the mode to stable shell.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210550911-30353853-3911-433f-91c0-2970f22412fb.png)


7. When i tried to list all the directories, we got many directories. But our interest here is to jump to the `Users` or `users` directory.
8. Let's see if we can find one.

> RESULT


