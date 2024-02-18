# Bon-nie-appetit
> Write-up author: jon-brandy

## DESCRIPTION:
After the successful hijacking of the D12 spaceship during the Space Pirate mission, 
the crew managed to place a signal transmitter on a vending machine that the Golden Fang's members are using to order 
food from the Supplier Spacecraft of Draeger. Golden Fang's crew's favorite food contains a secret ingredient called "Little Green People0," 
which we do not have further info about. The signal passes through many satellites before it reaches the Supplier, 
so it won't be easy to track the device and the leaked signal. Can you take advantage of it and get control of the Supplier?

## HINT:
- NONE

## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/52513364-507f-4862-b911-20fd90a244d5)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9cc12335-b63f-4968-9c1e-d12c16e242aa)


2. Decompiling the binary and reviewing the main() function, we can identified that the program has 5 menus.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/468eeb58-9bfa-4497-96ae-95ba613b8973)

#### MENUS:

```
1. Create chunks.
2. Show chunks.
3. Edit chunks.
4. Delete chunks.
5. Terminate program.
```

3. Reviewing the new_order() function, looks no bug resides here. It validates the maximum orders we can allocate is only 20 orders.
4. It accepts 2 datas, those are **size** and **contents**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7cc5f713-f55b-41e9-bfbf-0b224d948926)


5. Reviewing the show_order() function, seems there is no bug again. It accepts index and shows the chunk's content at that index.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eb40e0bd-0128-478a-86e7-1cff60abc231)


6. Reviewing the edit_order() function, we found a bug. Noticed it uses **strlen()** as the length of our input.
7. Remembering in C there is a NULL BYTE data, hence it's introduces a heap overflow using `OFF-ONE-BYTE` vulnerability.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2d6281b6-0ad8-4a3d-bd92-354364eca94b)


#### NOTES:

```
To trigger the overflow, we just need to fill the content to the fullest of it's size. For example if we edit the size to 0x60,
then we fill the content's up to 0x60, so there is an overflow because of the null-byte after it.

Remembering heap chunks are stored adjacent, if overflow occurs then current chunks will take the next chunk's
size into account.
```

8. Next, reviewing the delete_order() function, seems no use after free bug. The freed chunks are set to NULL.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cd398815-7ced-4ef7-96f8-89df916b8f3d)


