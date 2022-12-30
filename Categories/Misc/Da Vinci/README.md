# Da Vinci
> Write-up author: jon-brandy
## DESCRIPTION:
Try to find out the secret which is hiding inside of these pictures and learn the truth about Mona Lisa!
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210077219-fc23a929-ce9e-4515-a783-65182b34fa37.png)


2. Let's strings monalisa.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210077274-0a65b0cb-eb33-4b29-b536-654e5f56e7e1.png)


3. It looks like there are hidden files inside. Now extract it using binwalk, then jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210077423-dd7484c0-15e8-4fc9-a59d-bd7687c475bc.png)


4. Yep, just like what we thought!
5. Hmm.. let's try to unzip the `famous` one.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210077514-655246a8-441c-4c51-9ddd-9978ff4f3b0d.png)


6. Use `fcrackzip` to get the pass.

```sh
fcrackzip -D -u -p /usr/share/wordlists/rockyou.txt famous.zip
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210077594-0c2567f6-0afa-4ead-8f21-63290f3d4160.png)


7. Unzip it again.

![image](https://user-images.githubusercontent.com/70703371/210077669-3cb97800-6c66-474d-8a0e-04bc7ccb1360.png)


![image](https://user-images.githubusercontent.com/70703371/210077710-43accee0-98c0-4996-a29d-2e03b5dc5233.png)


8. Hmm.. let's use stegsolve.
9. Well i got nothing.
10. Let's try to strings `Plans.jpg`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210078206-b8ef1afc-346c-4c1a-afad-3b590f416382.png)


11. Check the youtube video.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210078287-f7fbd5b5-4020-42eb-aec4-a3c8b29fb271.png)


12. No clue.
13. Let's strings the last file.
14. Well got not clue either. But the file name caught my attention, the clue here is referring to `steghide` (?).
15. Let's try to use it and insert the pass as `TOM` ("TOM" is displayed at the image)

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210078864-d4441fed-af7e-49bc-bcab-8516d95f6f70.png)


16. There we go! Strings it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210078930-018e72e1-a29a-4fc3-9ebe-ee7e44559563.png)


17. Hmm.. What comes to my mind is, this password is for `Mona.jpg`. But first, the password looks like hashed (might be in MD5, since it's the common hash algorithm in CTF), try to crack it with online md5 cracker.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210079725-b0babbea-8f42-445b-ab42-41665f2738f2.png)


18. Let's use it to mona.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210079842-1c114675-f653-4eff-95ed-a96f7ff0c374.png)


