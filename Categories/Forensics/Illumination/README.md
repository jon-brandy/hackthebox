# Illumination
> Write-up author: jon-brandy
## DESCRIPTION:
A Junior Developer just switched to a new source control platform. Can you find the secret token?
## HINT:
- NONE
## STEPS:
1. First, unzip the file given, then jump to the extracted folder.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208028123-b07a6323-7f42-418c-a0db-afbe466dd916.png)


2. Looks like there's a hidden folder, go to that folder.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208028196-83e1fc3f-0d1f-4d4a-a3d3-9c582743fd70.png)


3. Based from the description, they want us to find the secret token.
4. The `.git` folder holds all the history changes.
5. Let's run git at this folder -> `git log`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208028405-f69ba97e-a1c1-4084-badb-ca3887d3e07e.png)


6. Notice at this commit.

![image](https://user-images.githubusercontent.com/70703371/208028499-9b47681e-0be2-452b-b0d4-0d6235483d52.png)


7. Sherlock removed the token.
8. To see what's removed we can run `git show 47241a47f62ada864ec74bd6dedc4d33f4374699`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208028695-f922eb41-ed05-4656-971a-30549e36c73e.png)


![image](https://user-images.githubusercontent.com/70703371/208028732-fe054bc8-1c09-4c5c-8ce3-1542193dfba1.png)


9. Based from the string's postfix, we can conclude that the text is encoded in base64.
10. Let's decode it!

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208028926-7869a84f-91da-406f-994e-19f022702851.png)


11. Got the flag!


## FLAG

```
HTB{v3rsi0n_c0ntr0l_am_I_right?}
```
