#!/bin/bash

# Настройки
APP_NAME="CurrencyExchange"
REPO_DIR="../$APP_NAME"
WWW_DIR="/var/www/$APP_NAME"
VENV_DIR="$WWW_DIR/venv"
SERVICE_FILE="/etc/systemd/system/$APP_NAME.service"

# Список файлов и папок для копирования
FILES_TO_COPY=(
    "src"
    "init_database.py"
    "LICENSE"
    "pyproject.toml"
    "README.md"
)

# Проверка прав
if [ "$EUID" -ne 0 ]; then
    echo "Запустите скрипт с sudo правами"
    exit 1
fi

# Проверка существования репозитория
if [ ! -d "$REPO_DIR" ]; then
    echo "Ошибка: Репозиторий $REPO_DIR не найден"
    exit 1
fi

# Создание директории приложения
echo "Создание директории $WWW_DIR..."
mkdir -p $WWW_DIR
chown -R www-data:www-data $WWW_DIR

# Копирование только указанных файлов
echo "Копирование файлов из $REPO_DIR в $WWW_DIR..."
for item in "${FILES_TO_COPY[@]}"; do
    if [ -e "$REPO_DIR/$item" ]; then
        echo "Копирование $item..."
        cp -r "$REPO_DIR/$item" $WWW_DIR/
    else
        echo "Предупреждение: $REPO_DIR/$item не существует"
    fi
done

# Установка правильных прав
chown -R www-data:www-data $WWW_DIR
chmod -R 755 $WWW_DIR

# Создание виртуального окружения
echo "Создание виртуального окружения..."
sudo -u www-data python3 -m venv $VENV_DIR

# Активация виртуального окружения и установка зависимостей
echo "Установка зависимостей Python из pyproject.toml..."
if [ -f "$WWW_DIR/pyproject.toml" ]; then
    # Установка build в виртуальном окружении
    sudo -u www-data $VENV_DIR/bin/pip install --upgrade pip
    sudo -u www-data $VENV_DIR/bin/pip install build

    # Создание wheel пакета и установка
    cd $WWW_DIR
    sudo -u www-data $VENV_DIR/bin/python -m build --wheel
    sudo -u www-data $VENV_DIR/bin/pip install dist/*.whl

    # Альтернатива: установка в режиме разработки
    # sudo -u www-data $VENV_DIR/bin/pip install -e .
else
    echo "Ошибка: pyproject.toml не найден"
    exit 1
fi

# Создание systemd сервиса
echo "Создание systemd сервиса..."
cat > $SERVICE_FILE << EOF
[Unit]
Description=Backend Application $APP_NAME
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$WWW_DIR
Environment=PYTHONUNBUFFERED=1
ExecStartPre=$VENV_DIR/bin/python $WWW_DIR/init_database.py
ExecStart=$VENV_DIR/bin/python -m app.server
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Перезагрузка systemd и запуск сервиса
echo "Активация сервиса..."
systemctl daemon-reload
systemctl enable $APP_NAME.service

echo "Запуск сервиса..."
systemctl start $APP_NAME.service

# Проверка статуса
echo "Проверка статуса сервиса..."
sleep 3
systemctl status $APP_NAME.service --no-pager

# Полезные команды для проверки
echo "
Установка завершена!

Для проверки логов используйте:
sudo journalctl -u $APP_NAME.service -f

Для перезапуска сервиса:
sudo systemctl restart $APP_NAME.service

Для проверки статуса:
sudo systemctl status $APP_NAME.service

Файлы приложения находятся в: $WWW_DIR
Виртуальное окружение в: $VENV_DIR
Service файл: $SERVICE_FILE
"