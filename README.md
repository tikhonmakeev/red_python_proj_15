Запуск проекта: 
- создайте venv и установите зависимости
```bash
python3 -m venv venv
```
```bash
venv/bin/pip install -r requirements.txt
```
- создайте файл config.env, с переменной окружения accuweather_token
Например такой, accuweather_token='your_token'
```bash
venv/bin/python3 web_app.py
```

Обработка ошибок:
- API-ключ достиг лимита
- Отсутствует интернет соединение
- Неверный формат ответа от сервера
- Неверное написание города от юзера
- Другие тоже обрабатываются, просто не так подробно