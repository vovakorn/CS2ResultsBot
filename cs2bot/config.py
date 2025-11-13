import os

# Токен бота берём из переменных окружения Yandex Cloud
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Канал по умолчанию — тоже из окружения (для v1 один канал)
DEFAULT_CHANNEL = os.getenv("TELEGRAM_CHAT_ID")

# Конфигурация каналов.
# Сейчас у нас один канал, который получает ВСЕ матчи.
# В будущем сюда можно добавить до 50 каналов для разных команд.
CHANNELS = [
    {
        "name": "global",           # просто метка для тебя
        "chat_id": DEFAULT_CHANNEL, # chat_id или @username канала
        "teams": None,              # None = без фильтра по командам
    },
    # Пример на будущее:
    # {
    #     "name": "NAVI",
    #     "chat_id": "@navi_results",
    #     "teams": ["Natus Vincere", "NaVi"],
    # },
]
