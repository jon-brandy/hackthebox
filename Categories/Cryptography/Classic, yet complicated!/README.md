# Classic, yet complicated!
> Write-up author: jon-brandy
## DESCRIPTION:
Find the plaintext, the key is your flag!
Flag format : HTB{key in lowercase}
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212460016-d5abc2f5-de7e-4437-b60f-af24bc01b26c.png)


![image](https://user-images.githubusercontent.com/70703371/212460023-cf652c7d-435d-466a-bc24-f291021f1ec9.png)


2. Let's paste the ciphertext to [this](https://www.boxentriq.com/code-breaking/cipher-identifier) website, so we know what ciphertext is this.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212460075-da5b81f4-0cda-490e-98c7-c103ad757fbc.png)


3. It's vigenere cipher! Now let's decode that using [dcode.fr](https://www.dcode.fr/vigenere-cipher).

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212460297-8ced8d72-0c34-41b5-a44a-8ad0137a1c11.png)


4. Based on the plaintext we got, we know that the key is `HELLOWORLD`, but based on the description, let's paste the string in lowercase as the flag.
5. Got the flag!

## FLAG

```
HTB{helloworld}
```
