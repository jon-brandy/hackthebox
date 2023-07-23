# APKrypt
> Write-up author: jon-brandy
## DESCRIPTION:
Can you get the ticket without the VIP code?
## HINT:
- NONE
## STEPS:
1. As usual, the problem setter recommend us to use the API >= 29 to install the apk.
2. Because we need to do zipalign and assign our keystore if we want to install it in API 33.
3. Since i only have the API 33, let's do zipalign and sign the key to our new apk.

#### NOTES:

```
To see the command used for zipalign - make our own keystore - sign the key to apk, open this writeup --> https://github.com/jon-brandy/hackthebox/blob/main/Categories/Mobile/APKey/README.md
```

4. Great let's install the apk using adb and open it on our emu.

> It asks us to input a VIP code and it seems we need to find the correct code.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/44e2709f-4442-459b-a39b-93440e518c04)


5. Let's decompile the apk with jadx-gui.

> INTEREST POINT (Main Activity).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0db36b9d-d4c0-482d-8bac-aea16c68df75)


6. Already tried to crack the hardcoded md5 with `crackstation` (online tools) but it didn't works, hence it seems we need to tamper the **if-statement**.
7. Let's decode the apk with `apktool`.

> COMMAND:

```
apktool d patched.apk
```

> JUMP TO THE VSCODE AND OPEN THE SMALI CODE.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bdf8e9ce-ecb2-4d02-97b2-3fca40633b68)


> What we want to patch (green box) - change it to nez.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a09859b9-a3d8-4aba-aaeb-ef7f23b1bf4d)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cc1563bc-cb2b-4bac-9f46-f0bc0466d06c)


> SAVE then, run this command to build the apk again.

```
apktool b -o patchedv1.2.apk patched
```

> Zipalign the apk again then sign it with apksigner.

```
zipalign -p 4 patchedv1.2.apk deploy_patched.apk
```

```
apksigner sign --ks a.keystore deploy_patched.apk
```

> Install the apk again, the input random strings. It will decrypt the flag, because our input's hash will not equal to the hardcoded hash.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a816c5b2-db63-4fd3-8938-346aa3d1e86c)


8. Got the flag!

## FLAG

```
HTB{3nj0y_y0ur_v1p_subscr1pt1on}
```


