# Templated
> Write-up author: jon-brandy
## DESCRIPTION:
Can you exploit this simple mistake?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208017009-400c8215-3d3c-435c-a33b-6a2683b533f7.png)


2. Actually the `<p>` tag value does give us a hint, we shall do RCE (Remote Code Execution) with python.
3. In jinja, python will evaluate any command inside the curly brackets.
4. Then it will appear in the HTML of the webpage.
5. To make sure of it, let's insert `config.items()` inside the curly brackets but first encode it into an url using cyberchef.

> ENCODED COMMAND TO URL

```
165.232.32.50:31397/%7B%7Bconfig.items()%7D%7D
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208018797-a54a741f-083b-4351-b5e9-de3141b2c9c1.png)


6. 
