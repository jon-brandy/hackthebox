# 0ld is g0ld
> Write-up author: jon-brandy
## DESCRIPTION:
Old algorithms are not a waste, but are really precious...
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210075600-5ee31745-9e09-4c37-a262-0ad80c26dffb.png)


2. Let's check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210075648-e5dddfda-b649-4096-b221-ce196180cd6a.png)


3. Anyway, open the pdf file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210076279-6e521433-90bb-4816-928e-00d361922bc9.png)


4. Seems we need to find the password.
5. Let's use `pdfcrack`.

```sh
pdfcrack -w /usr/share/wordlists/rockyou.txt -f '0ld is g0ld.pdf'
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210076586-58f4ca7c-5b40-404a-b142-f1a988f797bd.png)


6. Got the pass, use the pass now.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210076684-f542c920-83ed-4e3a-b696-31984335b0b1.png)


7. Notice there's something down there.

> RESULT - A MORSECODE

![image](https://user-images.githubusercontent.com/70703371/210076751-3ce88c7d-f320-4b05-a98a-506804e56875.png)


8. Copy it then decode it using [this](https://morsedecoder.com/) online tool.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210076856-2e072f04-da2f-46fb-b2ba-3ebe74ac089e.png)


9. Wrap it with `HTB{}`.
10. Got the flag.

## FLAG

```
HTB{R1PSAMU3LM0RS3}
```

