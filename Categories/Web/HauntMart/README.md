# HauntMart
> Write-up author: jon-brandy

## Lessons Learned:
- sdas

## DESCRIPTION:
HauntMart, a beloved Halloween webstore, has fallen victim to a curse, bringing its products to life. 
You must explore its ghostly webpages, and break the enchantment before Halloween night. 
Can you save Spooky Surprises from its supernatural woes?.

## HINT:
- NONE

## STEPS:
1. In this challenge we're given the source code of the webapp.

> WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/34f4b839-23ec-46bf-af6f-dd4df4a658d8)


2. Noticed there's a register option, hence the objective is to not bypass the login page or achieved admin role with bypassing the DB logic.
3. Upon registering an account, we're redirected to `/home` endpoint.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cbca3127-57f4-48e1-b571-d12a1c0c896b)


4. After clicking every available feature, turns out only one feature accessible. The sell product.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f4536a13-c409-4e82-8e34-a7f86cdc1a47)


5. Interesting! Let's review the source code handling the logic behind this endpoint.
