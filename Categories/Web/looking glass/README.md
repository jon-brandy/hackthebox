# looking glass
> Write-up author: jon-brandy
## DESCRIPTION:
We've built the most secure networking tool in the market, come and check it out!
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209566475-a7efbc7b-8a85-4907-bf4c-f4682b69bbe9.png)


2. Let's click the `ping` button.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209566539-85824af8-adb9-46ba-878b-35b6884b52d5.png)


3. Based from the output we got, i assume that on the server side, the command shall look like this:

```
ping -c 4 ip

or

system("ping -c 4 " + ip);
```

4. We can utilize the vulnerable here, by add a semicolon `;`.
5. By adding semicolon, then all the text behind it are interpreted as command.
6. Let's try to add `; ls` behind the ip value.

> Actuall command at the server side.

```sh
system("ping -c 4 142.93.37.215; ls");
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/209567067-96d3a895-e9d5-43ac-a888-a350b9cb2e29.png)

