# sozidateli_bot_team1
Проект телеграмм бота АНО Созидатели


# Запуск панели администратора
```
docker build -t admin .

docker run -p 8000:8000 admin
```

Внутри использован менеджер пакетов Poetry.
Чтобы работать с виртуальным окружением poetry локально, его нужно установить:
```
https://python-poetry.org/docs/master/#installing-with-the-official-installer
```
И далее в папке sozi_adm выполнить 
```
poetry install
```


