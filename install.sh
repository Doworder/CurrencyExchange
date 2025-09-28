#!/bin/bash

# Настройки
APP_NAME="CurrencyExchange"
REPO_DIR="./$APP_NAME"
WWW_DIR="/var/www/$APP_NAME"
SERVICE_FILE="/etc/systemd/system/$APP_NAME.service"
PYTHON_PATH="/usr/bin/python3"

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

# Установка зависимостей Python из pyproject.toml
if [ -f "$WWW_DIR/pyproject.toml" ]; then
    echo "Установка Python зависимостей из pyproject.toml..."

    # Проверяем, установлен ли build (необходим для установки из pyproject.toml)
    pip3 install --upgrade pip
    pip3 install build

    # Создаем wheel пакет и устанавливаем его
    cd $WWW_DIR
    python3 -m build --wheel
    pip3 install dist/*.whl

    # Альтернативный способ: установка в режиме разработки (если поддерживается)
    # pip3 install -e .
else
    echo "Предупреждение: pyproject.toml не найден, зависимости не установлены"
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
Environment=PYTHONPATH=$WWW_DIR
ExecStartPre=$PYTHON_PATH $WWW_DIR/init_database.py
ExecStart=$PYTHON_PATH -m app.server
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
systemctl start $APP_NAME.service

echo "Установка завершена! Статус сервиса:"
systemctl status $APP_NAME.service

# Полезные команды для проверки
echo "
Для проверки логов используйте:
journalctl -u $APP_NAME.service -f

Для перезапуска сервиса:
systemctl restart $APP_NAME.service

Для проверки статуса:
systemctl status $APP_NAME.service
"