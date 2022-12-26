# Spookifier
> Write-up author: jon-brandy
## DESCRIPTION:
There's a new trend of an application that generates a spooky name for you. 
Users of that application later discovered that their real names were also magically changed, causing havoc in their life. 
Could you help bring down this application?
## HINT:
- NONE
## STEPS:
1. Let's open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209550314-bf2c9973-9be9-414b-8cbd-ff537420b4ef.png)


2. Let's input `Hallo`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209550511-9a0f8bce-71fe-48dc-9c6c-667345089714.png)


3. Notice our input displayed as the parameter value.

![image](https://user-images.githubusercontent.com/70703371/209550550-5670a127-78d8-4535-8505-92be6b862090.png)


4. Let's try to input addition.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209550842-6ea4c1dc-368a-408a-b33a-92e18ca85414.png)


5. Based from the result we got, we can conclude that the website is vuln to **SSTI**.






## LEARNING REFERENCES:

```
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#mako
```
