# Wrong Spooky Season
> Write-up author: jon-brandy
## DESCRIPTION:
"I told them it was too soon and in the wrong season to deploy such a website, but they assured me that theming it properly would be enough to stop the ghosts from haunting us. 
I was wrong." Now there is an internal breach in the `Spooky Network` and you need to find out what happened. 
Analyze the the network traffic and find how the scary ghosts got in and what they did.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209421177-c0072551-f96f-4c62-9903-29ebd7f39381.png)


2. Strings the `.pcap` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209421190-84fd5a6b-ed5d-4d73-95ad-0d1db482b2f1.png)


3. Looks like there's a reversed `base64` encoded text.
4. Reverse the strings first, then decode it.

> REVERSE THE STRING

```cpp
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void)
{
    system("clear");
    char strings[] = {"==gC9FSI5tGMwA3cfRjd0o2Xz0GNjNjYfR3c1p2Xn5WMyBXNfRjd0o2eCRFS"};
    for(int i = strlen(strings); i >= 0; i--)
    {
        printf("%c", strings[i]);
    }


    return 0;
}
```

> OUTPUT

![image](https://user-images.githubusercontent.com/70703371/209421297-c6878abd-3da9-47de-b117-3a5f222d7c05.png)


> DECODE IT

![image](https://user-images.githubusercontent.com/70703371/209421305-a4c00eb4-9c20-4130-8cae-d44a3aaaf470.png)


5. Got the flag!

## FLAG

```
HTB{j4v4_5pr1ng_just_b3c4m3_j4v4_sp00ky!!}
```
