# CS2 Results Bot

Телеграм-бот, который по расписанию в Yandex Cloud Functions забирает последние результаты матчей CS2 из неофициального HLTV API и публикует их в каналы или чаты.

## Переменные окружения
| Название | Описание |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Токен вашего Telegram-бота, полученный у BotFather. |
| `TELEGRAM_CHAT_ID` | ID канала или чата, куда будут отправляться результаты. |

## Структура проекта
```
cs2bot/
    __init__.py
    config.py        # конфигурация каналов
    hltv_api.py      # работа с API результатов HLTV
    main.py          # handler(event, context)
requirements.txt     # зависимости (requests)
```

## Развёртывание в Yandex Cloud Functions
1. Соберите зависимости: `pip install -r requirements.txt -t packages/` и добавьте каталог `packages` к исходникам.
2. Упакуйте проект в архив и загрузите в функцию с runtime Python 3.10. Handler: `cs2bot.main.handler`.
3. Настройте таймерный триггер с нужным интервалом и задайте переменные окружения из таблицы выше.
