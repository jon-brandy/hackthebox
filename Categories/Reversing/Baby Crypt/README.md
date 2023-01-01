# Baby Crypt
> Write-up author: jon-brandy
## DESCRIPTION:
Give me the key and take what's yours.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Since we got a binary file, let's decompile it with ghidra.

> RESULT - MAIN FUNCTION

![image](https://user-images.githubusercontent.com/70703371/210162193-cddae9d1-bcf6-433b-b75f-5ea27985d38e.png)


3. Based from it we know that the key is 4 characters and there's a XOR algorithm.
4. It's a basic XOR concept, since the first 4 characters of the plaintext we want is `HTB{`, then we need to enter that as the key to XOR the flag.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210162323-f8fd20b1-90a5-4748-9d08-e163ff6f3658.png)


5. Now we're given the XOR. Simply enter copy the first 4 characters of the XORed characters as the key -> `w0wD`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210162350-56a931bd-90f9-4b4c-8413-8b5763131ac7.png)


6. Got the flag!

## FLAG

```
HTB{x0r_1s_us3d_by_h4x0r!}
```
