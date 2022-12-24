# WIDE
> Write-up author: jon-brandy
## DESCRIPTION:
We've received reports that Draeger has stashed a huge arsenal in the pocket dimension Flaggle Alpha. 
You've managed to smuggle a discarded access terminal to the Widely Inflated Dimension Editor from his headquarters, but the entry for the dimension has been encrypted. 
Can you make it inside and take control?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given and jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209441012-3f7f6795-71f3-4df0-a6f8-26f5983f8074.png)


2. Now run the binary file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209441046-f963e349-c2ec-4149-b79a-4b0aba574da4.png)


3. Hm.. Let's enter any number here (?)

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209441304-75490a1e-4594-42bf-9225-ee9ca0c003ce.png)


4. The program prompted us to enter the decryption key.
5. Let's decompile the file using ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209441334-8bd8908b-c291-4e41-a87c-26337ea0f956.png)


6. Let's check the `menu()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209441349-2dd9c316-171f-44f4-acdf-338bcfbef973.png)


7. Got the thing we are looking for there.

```
The decryption key -> sup3rs3cr3tw1d3
```

8. Enter the key.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209441378-1218007e-729f-4374-a694-f4065fa6ccf7.png)


9. Got the flag!

## FLAG

```
HTB{som3_str1ng5_4r3_w1d3}
```
