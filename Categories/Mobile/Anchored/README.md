# Anchored
> Write-up author: jon-brandy
## DESCRIPTION:
A client asked me to check if I can intercept the https request and get the value of the secret parameter that is passed along with the user's email. 
The application is intended to run in a non-rooted device. 
Can you help me find a way to intercept this value in plain text.
## HINT:
- NONE
## STEPS:
1. In this challenge we're given an apk file, noticed the README file says 2 notes to run this apk.

```
1. API leve 29 or earlier.
2. Non-rooted device.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bce29399-c132-427e-8a22-860ba3ed41fd)


2. I ran it on Pixel 4 API 25 (along with the google play) (non rooted).

> MOBILE APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e43174f6-167f-430a-b29b-2a8ebd9b577c)


3. Decompiled the apk using **JADX**, found an interesting endpoint at the `MainActivity` but sadly we can't access it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/25eabd3b-edeb-4c63-bc34-49ab13661b80)


4. Confused here, reviewing the `AndroidManifest.xml` source code, shall found an interesting attribute --> `android:networkSecurityConfig`.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eda9ac81-7643-4b48-af95-1489b9872ad8)


5. We can access the `network_security_config.xml` with this path --> `/res/xml/network_security_config.xml`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d89af009-336c-4d99-a3ae-2edcedd6a92a)


6. Searching on the internet about `network_security_config.xml exploit` shall resulting to this --> `https://gist.github.com/sunary/039d52ba3e71022f6062ad6a23d1c4ea`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a32477b5-3da4-4a78-b921-52c7ae3ed0bc)
 

7. After added the burpsuite cert to intercept request, we can't intercept the app.

#### NOTES:

```
If you use API under 30, name the burpsuite cert with .crt as it's extension.
```

8. This shall means, the intended solve should be patch the `network_security_config.xml` file.
9. Let's patch it.

> decode the apk with **apktool**.

```
apktool d Anchored.apk
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7aaf2826-ae11-4a8a-b417-557038f4b715)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3b83e4e4-acf0-4da6-acb7-056ce51f8aca)


> BUILD THE APK

```
apktool b -o anchored_patched.apk Anchored
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a78bc8dd-fd94-4e41-9f96-d691bca313ea)


> MAKE KEY

```
keytool -genkey -keystore a.keystore -keyalg RSA -keysize 2048 -validity 10000
```

> SIGN THE APK

```
apksigner sign --ks a.keystore anchored_patched.apk
```

10. Great! Now let's install the apk again with adb, then try to intercept the reqeust sent to server.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/667c98cb-dd60-4d75-bfcc-d0f6cfaea2da)


11. Got the flag!

## FLAG

```
HTB{UnTrUst3d_C3rT1f1C4T3s}
```

## BONUS

> Another network_security_config.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">anchored.com</domain>
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" overridePins="true"/>
        </trust-anchors>
    </domain-config>
</network-security-config>
```

