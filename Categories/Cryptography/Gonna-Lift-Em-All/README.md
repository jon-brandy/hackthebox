# Gonna-Lift-Em-All
> Write-up author: jon-brandy
## DESCRIPTION:
Quick, there's a new custom Pokemon in the bush called "The Custom Pokemon". Can you find out what its weakness is and capture it?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212736633-f39257de-5f7c-4c33-a3f5-71d0f4b136cb.png)


![image](https://user-images.githubusercontent.com/70703371/212736722-a4cabdca-181c-4a12-8f31-1eecfd850cae.png)


```py
from Crypto.Util.number import bytes_to_long, getPrime
import random

FLAG = b'HTB{???????????????????????????????????????????????????}'


def gen_params():
    p = getPrime(1024)
    g = random.randint(2, p - 2)
    x = random.randint(2, p - 2)
    h = pow(g, x, p)
    return (p, g, h), x


def encrypt(pubkey):
    p, g, h = pubkey
    m = bytes_to_long(FLAG)
    y = random.randint(2, p - 2)
    s = pow(h, y, p)
    return (g * y % p, m * s % p)


def main():
    pubkey, _ = gen_params()
    c1, c2 = encrypt(pubkey)

    with open('out.txt', 'w') as f:
        f.write(
            f'p = {pubkey[0]}\ng = {pubkey[1]}\nh = {pubkey[2]}\n(c1, c2) = ({c1}, {c2})\n'
        )


if __name__ == "__main__":
    main()

```

2. 
