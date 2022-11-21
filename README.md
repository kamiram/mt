# Mail Tracking

## Установка

Как обычно создаем **venv**

```
$ python -m venv venv
```

Инициализируем

```
$ source venv/bin/activate
```

Ставим Зависимости

```
$ pip install -U pip wheel
$ pip install -r req.txt
```

## Инициализация БД


```
$ flask --app flaskr init-db
```


## Запуск

```
$ source venv/bin/activate
$ flask --app flaskr --debug run
```

## Настройка акканута приложения google и extension
В [Google Console](https://console.cloud.google.com/apis/credentials):

Создать **OAuth client ID** для **Web Application **. Получить **CLIENT_ID** и **SECRET**.

Важно указать верный callback из **OAUTH_CALLBACK_URL**.  

Отредактировать **/instance/config.py**
```python
HOST_URL = 'https://mailtracker.mckira.com/t/'
OAUTH_CALLBACK_URL = 'https://mailtracker.mckira.com/callback'
GOOGLE_CLIENT_ID = '591404482299-bnqje8f040jelan59tqgpsnljgp2au3r.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'
```

## Настройка Extension

В файле **src/content.js** внизу поменять домен.

Пересобрать.

```
$ npm install
$ npm run build
```


Опция --debug - для отладки

## Настройка UWSGI

Примерный конфиг

```
[uwsgi]
plugins = python3
base = <Путь к проекту>

module = wsgi:app
chdir = %(base)
home = %(base)/venv
touch-reload = %(base)/restart

master = true
processes = 1
max-requests = 1000

vacuum = true
enable-threads = true
```

Положить в **/etc/uwsgi/app-enabled/mt.ini**

## Настройка NGINX

Конфиг

```
upstream uwsgi_mt_upstream {
        server unix:/var/run/uwsgi/app/mt/socket;
}       

server {
        server_name <Имя сервера>;            
        listen 80;
        listen [::]:80;

        location / {
                include uwsgi_params;
                uwsgi_pass uwsgi_mt_upstream;                         
        }       
}
```

Положить в **/etc/nginx/sites-enabled/mt**
