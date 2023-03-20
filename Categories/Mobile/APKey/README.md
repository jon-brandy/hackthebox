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

```xml
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

7. Based from it now we know that that `MainActivity` called first.
8. Let's check that.

> MainActivity

```java
package com.example.apkey;

import android.app.Activity;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import c.b.a.b;
import c.b.a.g;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/* loaded from: classes.dex */
public class MainActivity extends Activity {

    /* renamed from: b  reason: collision with root package name */
    public Button f927b;

    /* renamed from: c  reason: collision with root package name */
    public EditText f928c;
    public EditText d;
    public b e = new b();
    public g f = new g();

    /* loaded from: classes.dex */
    public class a implements View.OnClickListener {
        public a() {
        }

        @Override // android.view.View.OnClickListener
        public void onClick(View view) {
            Toast makeText;
            String str;
            try {
                if (MainActivity.this.f928c.getText().toString().equals("admin")) {
                    MainActivity mainActivity = MainActivity.this;
                    b bVar = mainActivity.e;
                    String obj = mainActivity.d.getText().toString();
                    try {
                        MessageDigest messageDigest = MessageDigest.getInstance("MD5");
                        messageDigest.update(obj.getBytes());
                        byte[] digest = messageDigest.digest();
                        StringBuffer stringBuffer = new StringBuffer();
                        for (byte b2 : digest) {
                            stringBuffer.append(Integer.toHexString(b2 & 255));
                        }
                        str = stringBuffer.toString();
                    } catch (NoSuchAlgorithmException e) {
                        e.printStackTrace();
                        str = "";
                    }
                    if (str.equals("a2a3d412e92d896134d9c9126d756f")) {
                        Context applicationContext = MainActivity.this.getApplicationContext();
                        MainActivity mainActivity2 = MainActivity.this;
                        b bVar2 = mainActivity2.e;
                        g gVar = mainActivity2.f;
                        makeText = Toast.makeText(applicationContext, b.a(g.a()), 1);
                        makeText.show();
                    }
                }
                makeText = Toast.makeText(MainActivity.this.getApplicationContext(), "Wrong Credentials!", 0);
                makeText.show();
            } catch (Exception e2) {
                e2.printStackTrace();
            }
        }
    }

    @Override // android.app.Activity
    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        setContentView(R.layout.activity_main);
        this.f927b = (Button) findViewById(R.id.button);
        this.f928c = (EditText) findViewById(R.id.editTextTextPersonName);
        this.d = (EditText) findViewById(R.id.editTextTextPassword);
        this.f927b.setOnClickListener(new a());
    }
}
```

9. At the `MainActivity`, the `onClick()` function seems shall be our interest now, because it shows us the login validation.

![image](https://user-images.githubusercontent.com/70703371/226258854-ad7f126a-803a-4b94-b6f3-94deaf54ed34.png)


10. The password cred seems hashed, hence the only cred we know is the username -> admin.
11. To bypass the login form, we can patch this if statement, by changing the statement from `eqz` to `nez`

![image](https://user-images.githubusercontent.com/70703371/226258977-1eca0e72-29b9-4677-b0ed-480c59b02167.png)


12. Let's decode the apk using apktool so we can patch the smali code.

> using apktool 

![image](https://user-images.githubusercontent.com/70703371/226259341-7d133b9f-37f3-406f-ae32-0a5ea51625bb.png)


13. Open the smali directory -> com -> example.apkey.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/226259525-6aab1e1f-b6c2-4982-ab0a-a1fc43197874.png)


14. Got 2 `MainActivity` files in smali, one has the onCreate function and the second one has the onClick function.
15. Comparing with the jadx, the if statement which we focusing is at this one:

![image](https://user-images.githubusercontent.com/70703371/226259903-0df7b11d-d134-49c9-a478-ef2bc1e1bc96.png)


16. Simply change the `if-eqz` to `if-nez`.

![image](https://user-images.githubusercontent.com/70703371/226259992-4084a162-72ec-417b-862c-285a038d5461.png)


17. Let's build the apk again using **apktool** then **zipalign** it again, next sign the app using **apksign**.

> apktool

![image](https://user-images.githubusercontent.com/70703371/226260132-957a7ea0-6003-4a93-accf-fc22e3fc0526.png)


> zipalign

![image](https://user-images.githubusercontent.com/70703371/226260238-7206d359-b932-4686-b585-34b4f722c86e.png)


> apksigner

![image](https://user-images.githubusercontent.com/70703371/226260271-d3af027b-6d88-45cb-9cb0-efcdfd72e580.png)


18. Install the apk file, then enter the username as `admin` and the password randomly.

![image](https://user-images.githubusercontent.com/70703371/226260463-75f1e6b2-b8ab-4098-a958-7eeff3fe24f8.png)


![image](https://user-images.githubusercontent.com/70703371/226260497-c7820250-2817-47c5-8f5c-f24655e80400.png)


19. Got the flag!

## FLAG

```

```



