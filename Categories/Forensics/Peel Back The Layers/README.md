# Peel Back The Layers
> Write-up author: jon-brandy
## DESCRIPTION:
A well known hacker rival of ours, managed to gain access to our dockehub profile and insert a backdoor to one of our public docker images in order to distribute his malware and fullfil his soul purpose, 
which is to destroy our steampunk robot using his steam malware. 
When we started tracing him back he deleted his backdoor. Can you help us retrieve his backdoor? Docker Image: `steammaintainer/gearrepairimage`
## HINT:
- NONE
## STEPS:
1. To solve this, let's pull the image using `docker` command.

```
docker pull steammaintainer/gearrepairimage
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209895997-6bf20d13-794a-465a-bb54-b123fc985f21.png)


2. Let's save the image to a `.tar` file.

```
sudo docker save steammaintainer/gearrepairimage > file.tar
```

> RESULT

