# Jerry
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, let's scan all open ports and services for the host given using nmap.

```
sudo nmap -p- -sVC -O 10.10.10.95
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210326505-71899f44-f1cb-4316-9b13-3f3cb4b1a13d.png)


2. Based from the output, there's only 1 port open, so we know what we're going to be attacking (port 8080).
3. Since the service is `HTTP` hence there must be a web server running.
4. Based on the service version, we can conclude that it's java web application.

> THE WEB APP

![image](https://user-images.githubusercontent.com/70703371/210327304-ab166588-acdd-481e-9379-5775b44e8a27.png)


5. When i clicked one of these buttons, i prompted to input username and password.

![image](https://user-images.githubusercontent.com/70703371/210327569-c0061bb7-900a-485d-ae35-307f9b8b12f5.png)


![image](https://user-images.githubusercontent.com/70703371/210327593-be4d82ce-41df-4519-811d-f589a2d7c290.png)


6. Our interest here is the `Manager app` so i did a small outsource about **APACHE TOMCAT MANAGER DEFAULT CREDS**.

> RESULT - GOT A GITHUB REPOSITORY

```
https://github.com/netbiosX/Default-Credentials/blob/master/Apache-Tomcat-Default-Passwords.mdown
```

![image](https://user-images.githubusercontent.com/70703371/210327887-8dc0da21-04ae-42ba-aa5c-683bfd55ce40.png)


7. Since the default creds not too many, so i bruteforce it every of it.
8. Logged in when i entered the username as `tomcat` and the pass as `s3cret`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210328200-0429966e-e8c3-483d-9f77-f3b7bb2f6807.png)


9. I think we can utilize this upload file feature.

![image](https://user-images.githubusercontent.com/70703371/210328421-87ebf759-3b0d-4b2d-9e39-02daa2f6520c.png)

> INFO

```
In software engineering, a WAR file (Web Application Resource or Web application ARchive) is a file used to distribute a collection of JAR-files, 
JavaServer Pages, Java Servlets, Java classes, XML files, tag libraries, static web pages (HTML and related files) and other resources that together 
constitute a web application. 
```

10.
