# Art
> Write-up author: jon-brandy
## DESCRIPTION:
Can you find the flag?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210081457-456a72be-049e-41aa-a6c7-3a34293fcdcc.png)


2. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210081484-42baa9ff-9993-4f20-8ce9-5306091145ef.png)


3. Since it's `png` file, we can use **zsteg**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210081546-49808faa-1683-49f0-b211-771e72071d73.png)


![image](https://user-images.githubusercontent.com/70703371/210082197-19c8212e-38f9-43ee-a1c2-3f59fc17d98a.png)


4. Still got nothing.
5. Now let's see the image.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210082666-3bda92f9-2798-43f4-8317-6590371a5b28.png)


6. What comes to my mind is `PIET programming languange`.
7. Well we can use [this](https://www.bertnase.de/npiet/npiet-execute.php) online interpreter.
8. Upload the image to the website.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210083008-556bdfdd-59a7-46c1-8afe-76ab94541452.png)


9. Got the flag!

## FLAG

```
HTB{p137_m0ndr14n}
```
