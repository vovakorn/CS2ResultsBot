# CS2 Results Bot for Yandex Cloud Functions

Минимальный Python-проект, который раз в N минут запускается как Yandex Cloud Function,
ходит в неофициальный HLTV API и публикует последние результаты матчей CS2 в Telegram.

## Структура
```
cs2bot/
    __init__.py
    config.py        # конфигурация каналов
    hltv_api.py      # работа с API результатов
    main.py          # handler(event, context)
requirements.txt     # зависимости (requests)
```

## Настройка
1. Создайте Telegram-бота и получите токен (`TELEGRAM_BOT_TOKEN`).
2. Узнайте ID канала/чата (`TELEGRAM_CHAT_ID`) куда бот будет писать.
3. Установите переменные окружения в Yandex Cloud Functions:
   * `TELEGRAM_BOT_TOKEN`
   * `TELEGRAM_CHAT_ID`
4. (Опционально) отредактируйте `cs2bot/config.py`, добавив до 50 объектов
   `TelegramChannel` для нескольких каналов.

## Деплой
1. Установите зависимости `pip install -r requirements.txt -t ./packages` и запакуйте
   код с каталогом `packages` в zip-архив.
2. Создайте Yandex Cloud Function на Python 3.10 и укажите handler `cs2bot.main.handler`.
3. Настройте таймерный триггер на нужный интервал (например, каждые 5 минут).

Функция вернёт JSON с информацией об отправленных матчах или статус ошибки.
