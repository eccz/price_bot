# price_bot
Сервис для отправки оповещений в Telegram по котировкам позиций на binance и Tinkoff.

## Описание
Для корректной работе сервиса потребуется:
* Разобраться в Google Developers Console, создать там проект и сгенерировать файл-ключ для доступа через API. Подробная инструкция изложена в этом видео: https://www.youtube.com/watch?v=9XdNny1DqXE. Файл-ключ должен находиться в корне директории /dev.
* Данные по котировкам заносятся пользователем через Google-таблицы. Образец таблицы https://docs.google.com/spreadsheets/d/1gWjY7u6_dTmrQo-BXRgb3l80uq-876Or7v0QiQEiIgM/edit?usp=sharing. Работа сервиса привязана к конкретным столбцам. Такую же таблицу необходимо создать у себя и выдать необходимые права доступа.
* Получить токен Тинькофф-инвестиций. Сервис проводит операции только по получению котировок.
* Получить токен Telegram-бота, который будет отправлять сообщения.
* Найти с помощью бота @getmyid_bot требуемые chatID пользователей Telegram, которым будут отправляться оповещения.
* Создать файл creds.py по примеру "example_creds.py". Файл creds.py должен находиться в корне директории /dev.
* Установить необходимые библиотеки в окружение из requirements.txt

**Точкой входа в приложение является файл main.py в директории /dev.**

---
Получение котировок с Binance реализовано через websocket. Websocket бинанса держится не более суток, процесс нужно перезапускать. 
На сервере использовал для этого supervisord - два активных процесса: основной - main.py и процесс, перезагружающий основной bash-скриптом и спящий нужное количество времени.
