# baby CachedView
> Write-up author: jon-brandy
## DESCRIPTION:
I made a service for people to cache their favourite websites, come and check it out! But don't try anything funny, 
after a recent incident we implemented military grade IP based restrictions to keep the hackers at bay...
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209827040-82750d85-6508-48a1-9a44-dbbf3c0493aa.png)


2. When i tried to do simple xss attack.
3. Seems failed.
4. Let's download the source code given.

![image](https://user-images.githubusercontent.com/70703371/209827912-da2b5839-54f8-43f1-b7ab-37430257f16e.png)


5. There's a flag png.

> FLAG.PNG

![image](https://user-images.githubusercontent.com/70703371/209827980-31a73e8f-d4e8-45ab-8d68-5f30e289d316.png)


6. What comes to my mind after saw this image is we shall do DNS rebinding attack.
7. Next, when i tried to analyze the `routes.py` and `util.py` script.

> ROUTES.PY

```py
from flask import Blueprint, request, render_template, abort, send_file
from application.util import cache_web, is_from_localhost
web = Blueprint('web', __name__)
api = Blueprint('api', __name__)
@web.route('/')
def index():
    return render_template('index.html')
@api.route('/cache', methods=['POST'])
def cache():
    if not request.is_json or 'url' not in request.json:
        return abort(400)
    
    return cache_web(request.json['url'])
@web.route('/flag')
@is_from_localhost
def flag():
    return send_file('flag.png')
```

> UTIL.PY

```
import functools, signal, struct, socket, os
from urllib.parse import urlparse
from application.models import cache
from flask import request, abort
generate = lambda x: os.urandom(x).hex()
def flash(message, level, **kwargs):
    return { 'message': message, 'level': level, **kwargs }
def serve_screenshot_from(url, domain, width=1000, min_height=400, wait_time=10):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-sync')
    options.add_argument('--disable-translate')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--metrics-recording-only')
    options.add_argument('--no-first-run')
    options.add_argument('--safebrowsing-disable-auto-update')
    options.add_argument('--media-cache-size=1')
    options.add_argument('--disk-cache-size=1')
    options.add_argument('--user-agent=MiniMakelaris/1.0')
    options.preferences.update(
        {
            'javascript.enabled': False
        }
    )
    driver = webdriver.Firefox(
        executable_path='geckodriver',
        options=options,
        service_log_path='/tmp/geckodriver.log',
    )
    driver.set_page_load_timeout(wait_time)
    driver.implicitly_wait(wait_time)
    driver.set_window_position(0, 0)
    driver.set_window_size(width, min_height)
    driver.get(url)
    WebDriverWait(driver, wait_time).until(lambda r: r.execute_script('return document.readyState') == 'complete')
    filename = f'{generate(14)}.png'
    driver.save_screenshot(f'application/static/screenshots/{filename}')
    driver.service.process.send_signal(signal.SIGTERM)
    driver.quit()
    cache.new(domain, filename)
    return flash(f'Successfully cached {domain}', 'success', domain=domain, filename=filename)
def cache_web(url):
    scheme = urlparse(url).scheme
    domain = urlparse(url).hostname
    if not domain or not scheme:
        return flash(f'Malformed url {url}', 'danger')
        
    if scheme not in ['http', 'https']:
        return flash('Invalid scheme', 'danger')
    def ip2long(ip_addr):
        return struct.unpack('!L', socket.inet_aton(ip_addr))[0]
    
    def is_inner_ipaddress(ip):
        ip = ip2long(ip)
        return ip2long('127.0.0.0') >> 24 == ip >> 24 or \
                ip2long('10.0.0.0') >> 24 == ip >> 24 or \
                ip2long('172.16.0.0') >> 20 == ip >> 20 or \
                ip2long('192.168.0.0') >> 16 == ip >> 16 or \
                ip2long('0.0.0.0') >> 24 == ip >> 24
    
    if is_inner_ipaddress(socket.gethostbyname(domain)):
        return flash('IP not allowed', 'danger')
    
    return serve_screenshot_from(url, domain)
def is_from_localhost(func):
    @functools.wraps(func)
    def check_ip(*args, **kwargs):
        if request.remote_addr != '127.0.0.1' or request.referrer:
            return abort(403)
        return func(*args, **kwargs)
    return check_ip
```

8. Based from the **@api.route** params, we know that the first endpoint is at `/cache` and accepts a url (JSON over POST).
9. Next, will take a screenshot of the provided URL using a headless web browser.
10. Then, return the image(flag.png).
11. The second endpoint is at `/flag`, simply returns the `flag.png` image.
12. Next we can see that there's a validation to check whether the request.remote_addr is from "127.0.0.1" or not.
13. Remember at the image there's a string "TOCTOU".

```
Time of Check to Time of Use
```

14. 
