# Vault-breaker
> Write-up author: jon-brandy
## DESCRIPTION:
Money maker, Big Boy Bonnie has a crew of his own to do his dirty jobs. In a tiny little planet a few lightyears away, a custom-made vault has been found by his crew. 
Something is hidden inside it, can you find out the way it works and bring it to Bonnie?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212217786-3c2fb825-ebf7-4425-93b9-64317a4e71d5.png)


![image](https://user-images.githubusercontent.com/70703371/212217827-6a97d700-4568-47b5-9c7a-2f58794b5834.png)


![image](https://user-images.githubusercontent.com/70703371/212217857-cdd7f638-56c3-4599-abbb-4c3cbb562de1.png)


2. Hmm.. All protections enabled, let's decompile the binary then.

> RESULT - MAIN

![image](https://user-images.githubusercontent.com/70703371/212218234-c0d5b618-c822-404e-ac2b-4307e6119d43.png)


3. Based from the `secure_password()` function, we know that the flag is XORed with random key.

![image](https://user-images.githubusercontent.com/70703371/212219103-3bd915ae-2ac2-492c-93ac-a98e399d0010.png)


4. Notice we have an option to generate new random key of given size before dump the XORed flag.

![image](https://user-images.githubusercontent.com/70703371/212219064-35484247-42e0-409e-8f37-2ba8cd7ef142.png)


5. When analyzing the `new_key_gen()` function, see the vuln is at the **strcpy** function.

![image](https://user-images.githubusercontent.com/70703371/212220104-38ded8d2-8f29-4df3-a4c1-1b91494a8dae.png)


6. Hence we can utilize that and leak the flag byte by bytes.



