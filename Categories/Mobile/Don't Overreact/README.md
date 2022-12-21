# Don't Overreact
> Write-up author: jon-brandy
## DESCRIPTION:
Some web developers wrote this fancy new app! It's really cool, isn't it?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208849896-b369a56d-70ce-43ff-9ad4-eeb19d60c587.png)


2. To reverse engineer APK file, i used `apktool`.

##### COMMAND -> `apktool d app-release.apk`

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208850296-36ca559f-4dea-4327-b6e1-2b2b499c5e2e.png)


![image](https://user-images.githubusercontent.com/70703371/208850677-c473d101-ee4d-42f5-81df-839a0c6c919b.png)


3. Jump to the folder.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208850782-35c85f7f-2047-4782-92ac-5154fbd45d51.png)


4. Let's check the `assets` directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/208851248-940df5ad-80a5-4ba5-a906-8877d78124f6.png)


5. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208851308-180829f5-dfe3-42bb-bf8c-4fecfff2f215.png)


6. Try to combine strings with grep to find the flag prefix.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208851451-83a98444-68d0-4244-997a-93a0c2046a33.png)


7. Didn't find it, but a string caught my attention.

```
SFRCezIzbTQxbl9jNDFtXzRuZF9kMG43XzB2MzIyMzRjN30=
```

8. Looks like a base64 encoded text.
9. Decode it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208851669-ef75798a-f2d5-4e59-abe5-9560940d1f73.png)


10. Got the flag!

## FLAG

```
HTB{23m41n_c41m_4nd_d0n7_0v32234c7}
```
