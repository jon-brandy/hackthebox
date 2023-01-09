# Eternal Loop
> Write-up author: jon-brandy
## DESCRIPTION:
Can you find a way out of this loop?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211326692-beae9c99-4c49-43c4-8a2f-7a75bd488a2f.png)


2. Hmm.. Let's unzip it again.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211326818-e24b3876-1b6c-4e86-9de7-5f6fa1bdadd3.png)


3. It seems we can't enter the same password as before.
4. Let's use `fcrackzip` then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211327263-40ce1047-a001-4d2d-96fc-08a418e57c61.png)


5. Got no result, so i tried to unzip it using it's own name as the password. Turns out got it right!

![image](https://user-images.githubusercontent.com/70703371/211328113-94f2568e-ca86-4e69-ad85-e0046c1b59d0.png)


6. Let's keep going.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211328392-8a60111e-d7b1-47d9-97f2-8cfe86b957dd.png)


7. Seems we need to automate this. So i did a small outsource on the internet for a script to automate this unzipping. Found this bash script.

```sh
#!/bin/bash

ZIPFILE=$1
RESULT=0

while [ $RESULT -eq 0 ]
do
PASSWORD=$( unzip -l $ZIPFILE | grep -E "^\s+[0-9]+" | grep -Eo "[0-9]+\.zip" | grep -Eo "[0-9]+" )
unzip -P "$PASSWORD" "$ZIPFILE"
RESULT=$?
ZIPFILE="$PASSWORD.zip"
done
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211329788-8735e317-7ad6-4813-a317-7ebd8c69d6a4.png)


8. Stopped at 6969.
9. Let's use **fcrackzip** for it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211329990-9da3c456-6a09-41dd-9e71-5cf2972ceeb5.png)


> USE THE PASS, THEN STRINGS THE FILE WE GOT - RESULT

![image](https://user-images.githubusercontent.com/70703371/211330191-fb620c18-0017-49cf-8779-23d6cb0e3a78.png)


10. Got the flag!


## FLAG

```
HTB{z1p_and_unz1p_ma_bruddahs}
```



