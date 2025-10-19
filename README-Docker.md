# Установка и запуск приложения через Docker Compose

## Подготовка

1. Установите Docker и Docker Compose на вашей системе
2. Скопируйте репозиторий на вашу локальную машину

## Настройка переменных окружения

1. Создайте файл `.env` в корне проекта, основываясь на примере из `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. Отредактируйте файл `.env`, указав ваши собственные значения:
   - `TELEGRAM_API` - API ключ для Telegram бота
   - `HIVEOS_API` - API ключ для Hive OS
   - `TUYA_API_KEY` - API ключ для Tuya Cloud
   - `TUYA_API_SECRET` - API секрет для Tuya Cloud
   - `TUYA_DEVICE_ID` - ID устройства Tuya
   - `TUYA_REGION` - Регион Tuya (например, "eu", "us", "cn")
   - `CHAT_ID` - ID чата Telegram для уведомлений
   - `PAUSE` - Пауза между циклами работы (в секундах)
   - `MINUTES_WINDOW` - Временное окно для стартового часа

## Запуск приложения

1. Убедитесь, что вы находитесь в корне проекта, где находится файл `docker-compose.yml`

2. Запустите приложение:
   ```bash
   docker-compose up -d
   ```

3. Для просмотра логов:
   ```bash
   docker-compose logs -f tuya-smart-socket
   ```

## Остановка приложения

```bash
docker-compose down
```

## Обновление приложения

1. Обновите файлы приложения:
   ```bash
   git pull
   ```

2. Пересоберите образ:
   ```bash
   docker-compose up -d --build
   ```

## Структура сервисов

- `tuya-smart-socket` - основной сервис приложения
- Используется volume `db_data` для сохранения данных базы данных
- Для работы приложения требуется файл `.env` с настройками