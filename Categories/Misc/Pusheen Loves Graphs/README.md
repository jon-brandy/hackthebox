# Pusheen Loves Graphs
> Write-up author: jon-brandy
## DESCRIPTION:
Pusheen just loves graphs, Graphs and IDA. Did you know cats are weirdly controlling about their reverse engineering tools? Pusheen just won't use anything except IDA.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210083591-b6040cea-3c71-4cdb-9dae-f1b8444e4ba0.png)


2. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210083621-9095d736-ae52-412d-8076-75d3a32329eb.png)


3. Now we know it's a 32 Bit binary file and not stripped, since it's not stripped, hence it's easier for us to debug the binary flow, because we can read the functions names.
4. Now check the binary's protection.

> RESULT - PARTIAL RELRO - NO PIE - NX DISABLED - NO CANARY FOUND

![image](https://user-images.githubusercontent.com/70703371/210084143-651329ba-03e8-4c25-ab41-d97a5d405731.png)


5. But anyway, let's decompile the binary using IDA (32 BIT).

> RESULT

