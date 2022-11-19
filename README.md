# Mail Tracking

## Установка

Как обычно создаем venv

`
$ python -m venv venv
`

Инициализируем

`
$ source venv/bin/activate
`

Ставим Зависимости

`
$ pip install -U pip wheel
$ pip install -r req.txt
`

## Инициализация БД


`
$ flask --app flaskr init-db
`


## Запуск

`
$ source venv/bin/activate
$ flask --app flaskr --debug run
`

## Настройка Extension

В файле src/content.js внизу поменять домен.

Пересобрать.

`
$ npm install
$ npm run build
`


Опция --debug - для отладки

## Настройка UWSGI

Примерный конфиг

`
[uwsgi]
plugins = python3
base = <Путь к проекту>

module = app:app
chdir = %(base)
home = %(base)/venv
touch-reload = %(base)/restart

master = true
processes = 1
max-requests = 1000

vacuum = true
enable-threads = true
`

Положить в /etc/uwsgi/app-enabled/mt.ini

## Настройка NGINX

Конфиг

`
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
`

