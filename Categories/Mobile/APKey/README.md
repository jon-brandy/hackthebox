# APKey
> Write-up author: jon-brandy
## DESCRIPTION:
This app contains some unique keys. Can you get one?
## HINT:
- NONE
## STEPS:
1. Given an APK file, let's try to install it to our emulator.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/226255408-10da79a9-aa99-40ae-b139-edc1c9603095.png)


2. Seems we need to zipaligned the file using **zipalign**.

> Using zipalign

```
zipalign -p 4 APKey.apk newapp.apk
```

![image](https://user-images.githubusercontent.com/70703371/226255632-61400982-16f3-4e7a-a0b2-ae04fe02626a.png)


3. Then let's make a keystore and sign it to the apk file.

> Using keystore

```
keytool -genkey -keystore a.keystore -keyalg RSA -keysize 2048 -validity 10000
```

> Using apksigner

```
apksigner sign --ks a.keystore newapp.apk
```

> RESULT after installing it using htb

![image](https://user-images.githubusercontent.com/70703371/226256701-321b203a-3611-413e-a07b-2ea6c113f9cf.png)


4. Let's enter both username and password as admin.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/226257282-6110c2fd-1437-4bd7-af96-0798cc600a7c.png)


5. Hmm.. Now let's decompile the apk file using jadx.
6. Let's jump to the `androidManifest.xml` to check what activity is running at the start.

> RESULT

```
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" android:versionCode="1" android:versionName="1.0" android:compileSdkVersion="30" android:compileSdkVersionCodename="11" package="com.example.apkey" platformBuildVersionCode="30" platformBuildVersionName="11">
    <uses-sdk android:minSdkVersion="16" android:targetSdkVersion="30"/>
    <application android:theme="@style/Theme.APKey" android:label="@string/app_name" android:icon="@mipmap/ic_launcher" android:allowBackup="true" android:supportsRtl="true" android:roundIcon="@mipmap/ic_launcher_round" android:appComponentFactory="androidx.core.app.CoreComponentFactory">
        <activity android:name="com.example.apkey.MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
```

7. Based from it now we know that  
