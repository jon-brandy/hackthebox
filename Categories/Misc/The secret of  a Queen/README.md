# The secret of a Queen
> Write-up author: jon-brandy
## DESCRIPTION:
Decrypt the code and find the Queen's secret!
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210125138-fe4535f9-c2dc-418d-9402-f8824baeebca.png)


2. Check the file type, to make sure it's really is png or not.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210125148-6998b3fe-1f04-4910-96f3-66f8158f47b2.png)

3. It's really is, now let's use zsteg.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210125177-7259ce66-8bd3-413e-9814-64cf8d693a1a.png)


4. Got nothing.
5. I did binwalk, foremost and got no hidden files inside.
6. Let's see the image then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210125221-c18423ca-b3cb-4fba-bd2a-9984b4e57d4a.png)


7. Confused what's this.
8. So i did a small outsource.
9. Turns out it's a **MARY STUART CODE**.
10. I use [this](https://www.dcode.fr/mary-stuart-code) online tool to decode the code.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210125353-2f76dbd9-60db-4f34-8e27-fd32ab0caf67.png)


11. Hmm.. The plaintext we got give us the wrong flag. 

```
HTB{THEBABINGTONPASOT}
```

12. So i did a small outsource again about babington - queen mary and found this.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210125458-d71754d9-6145-402a-80c4-e51cdfeb6d6a.png)


13. Got us the correct flag!

## FLAG

```
HTB{THEBABINGTONPLOT}
```
