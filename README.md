# Проект “Обмен валют”
REST API для описания валют и обменных курсов. Позволяет просматривать и редактировать списки валют и обменных курсов, и совершать расчёт конвертации произвольных сумм из одной валюты в другую.

Веб-интерфейс для проекта не подразумевается.
### Installation on PC

1) Склонировать репозиторий
```shell
git clone https://github.com/Doworder/CurrencyExchange.git
```
2) Перейти в папку проекта
```shell
cd CurrencyExchange
```
3) Создать виртуальное окружение
```shell
python -m venv venv
```
4) Активировать виртуальное окружение
Windows

```shell
venv\Scripts\activate.bat
```

Linux и MacOS

```shell
source venv/bin/activate
```
5) Установить пакет
```shell
pip install .
```

### Installation on VPS
0) Необходимо установить зависимости:
```shell
git
python3.12
pip
venv
```

1) Склонировать репозиторий
```shell
git clone https://github.com/Doworder/CurrencyExchange.git
```
2) Перейти в папку проекта
```shell
cd CurrencyExchange
```
3) Запустить скрипт
```shell
bash install.sh
```
- Скрипт установит файлы проекта 
```commandline
/var/www/CurrencyExchange
```
 - Установит права для директории и файлов.
 - Создаст systemd сервис.

#### Команды для управления сервисом:
Для проверки логов используйте:
```shell
journalctl -u $APP_NAME.service -f
```

Для перезапуска сервиса:
```shell
systemctl restart $APP_NAME.service
```

Для проверки статуса:
```shell
systemctl status $APP_NAME.service
```
