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


7. It seems there's only one file and no directory in the current directory.
8. Let's check the root directory by add -> `; ls /`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209567290-ec4fa5fe-ef1a-4c00-b16c-b6043ffbed8a.png)


![image](https://user-images.githubusercontent.com/70703371/209567359-56bd09ac-3deb-4891-91f5-18f83e719833.png)


![image](https://user-images.githubusercontent.com/70703371/209567384-f85d2262-29ff-4427-b96c-232e7c7cfe8e.png)


![image](https://user-images.githubusercontent.com/70703371/209567390-c45a527b-88a2-4f5a-a9d6-940372d2b243.png)


9. Notice there's a directory/file named **flag_50j98**.
10. Since we don't know whether it's a directory or a file, let's test if it's a file or not by run cat.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209567530-530384dc-ad24-4e89-9048-385154f69755.png)


![image](https://user-images.githubusercontent.com/70703371/209567570-362d06f0-f2cb-4716-9753-3abc4334d1ac.png)


11. Got the flag!

## FLAG

```
HTB{I_f1n4lly_l00k3d_thr0ugh_th3_rc3}
```
