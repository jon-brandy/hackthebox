# Ancient Encodings
>Write-up author: ptr173

## DESCRIPTION:
Your initialization sequence requires loading various programs to gain the necessary knowledge and skills for your journey. Your first task is to learn the ancient encodings used by the aliens in their communication.

## HINT:
- NONE

## STEPS:
1. First unzip the given attachment and we will get source.py and the output.txt

source.py
```python
from Crypto.Util.number import bytes_to_long
from base64 import b64encode
from secret import FLAG


def encode(message):
    return hex(bytes_to_long(b64encode(message)))


def main():
    encoded_flag = encode(FLAG)
    with open("output.txt", "w") as f:
        f.write(encoded_flag)


if __name__ == "__main__":
    main()
```

output.txt
```
0x53465243657a51784d56383361444e664d32356a4d475178626a6c664e44497a5832677a4d6a4e664e7a42664e5463306558303d
```

2. In the source code, we can see the code is used to encode the flag to base64 and then encode it again to hex and the result is written in the output.txt
3. So we just need to decode the output from hex to strings and decode it again using base64 and we will get the flag. I am using cyberchef to decode the output

![image](https://github.com/Bread-Yolk/hackthebox/assets/123644468/10fe46ce-2aa7-4c4f-a968-beff523f34df)

## FLAG
HTB{411_7h3_3nc0d1n9_423_h323_70_574y}
