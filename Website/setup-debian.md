I've spent a while trying to rewrite my website into something a bit more interesting (i.e., difficult and head-achy) to maintain. I also wanted to try implementing things like a comments section and a publishing system that I can access from an admin portal.

# The backend

After playing around with some web frameworks in C++ and Java, I landed on Python using FastAPI and a SQLite backend. I've not loved using Python in the past, but I have to admit that it was incredible how easy it is to haphazardly prototype and get something shuffling along. While it does make me cringe a bit as I definitely have taken advantage and produced some ugly code... I actually got something done.

# The frontend

I hated writing the frontend. I chose to just use TailwindCSS and nothing else. It gives you a lot to play around with, but I'm not very good at getting CSS working properly so I'm not sure how maintainable this whole ball of bunched together tailwind classes attached to divs is going to be in the longer term.

# Deploying the site

To deploy the site I got myself a Linode VPS. Here are the setup steps below (this is mostly for myself to remember what the heck I did a year from now).

1. Install Dependencies

```
apt update
apt upgrade
apt install pipenv git certbot python3-certbot-apache apache2
```

2. Create a user for running the site
```
adduser nathanieljwright-com
su - nathanieljwright-com
```

3. Clone and setup project
```
git clone https://github.com/N8-Wright/N8
cd N8
pipenv sync
cd src
pipenv run uvicorn website:app --host 0.0.0.0 --port 8080 --proxy-headers --forwarded-allow-ips '{Your VPS IP}'
```

4. Enable Apache modules for reverse proxy
```
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_ajp
a2enmod rewrite
a2enmod deflate
a2enmod headers
a2enmod proxy_balancer
a2enmod proxy_connect
a2enmod proxy_html
```

5. Modify /etc/apache2/sites-enabled/000-default.conf

```
<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	ProxyPreserveHost On
	ProxyPass / http://0.0.0.0:8080/
	ProxyPassReverse / http://0.0.0.0:8080/
</VirtualHost>


<VirtualHost *:443>
	ProxyPreserveHost On
	ProxyPass / http://0.0.0.0:8080/
	ProxyPassReverse / http://0.0.0.0:8080/

	RequestHeader set "X-Forwarded-Proto" expr=%{REQUEST_SCHEME}
</VirtualHost>
```

6. Running certbot

```
certbot --apache
```


