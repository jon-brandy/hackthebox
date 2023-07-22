# Pinned
> Write-up author: jon-brandy
## DESCRIPTION:
This app has stored my credentials and I can only login automatically. I tried to intercept the login request and restore my password, but this seems to be a secure connection. Can you help bypass this security restriction and intercept the password in plaintext?
## HINT:
- NONE
## STEPS:
1. Based from the description and the chall's title, it seems we just need to bypass the ssl pinner applied.
2. Unzipping the .zip file, there's a .txt file telling that we need to use the API under 29 or exact 29.
3. But since i only have the API 33, hence let's just try it.

> Need to do zipalign --> 4 bytes. || this is the reason they told us to use the API >= 29.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ee1c2d60-2b2f-48a9-b580-31b7c034bc0c)

> zipalign

```
zipalign -p 4 pinned.apk patched_pinned.apk
```

> Make keystore

```
keytool -genkey -keystore a.keystore -keyalg RSA -keysize 2048 -validity 10000
```

> Apply keystore

```
apksigner sign --ks a.keystore patched_pinned.apk
```

4. After signed the apk, then install the apk.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ae1519a0-18c5-4c01-b935-1af1d2c4ae95)


5. Let's run the app.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4aa25d14-49ad-46cf-9c2b-7491079f8443)


6. Hmm.. It seems there's nothing we can do here. After clicked the login, it saya "logged in". Based from the description we just need to intercept the request so we can see what is the password.
7. To bypass the ssl pinning, i used this frida codeshare --> https://codeshare.frida.re/@pcipolloni/universal-android-ssl-pinning-bypass-with-frida/

> COMMAND

```
frida --codeshare pcipolloni/universal-android-ssl-pinning-bypass-with-frida -f com.example.pinned -U 
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6d97759a-918f-4c08-8af1-bb34bf1e6e2d)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/741b6dc5-62e8-47f2-9d31-332f177bf148)


8. Got the flag!

## FLAG

```
HTB{trust_n0_1_n0t_3v3n_@_c3rt!}
```

