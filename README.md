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

Опция --debug - для отладки

