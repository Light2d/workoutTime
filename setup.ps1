
# Создание виртуального окружения
Write-Host "Создаю виртуальное окружение..."
python -m venv .venv

# Активация виртуального окружения
Write-Host "Активирую виртуальное окружение..."
& .\.venv\Scripts\Activate.ps1

# Установка зависимостей
if (Test-Path "requirements.txt") {
    Write-Host "Устанавливаю зависимости из requirements.txt..."
    pip install -r requirements.txt
} else {
    Write-Host "Файл requirements.txt не найден. Пропускаю установку зависимостей." -ForegroundColor Yellow
}

# Выполнение миграций
if (Test-Path "manage.py") {
    Write-Host "Выполняю миграции..."
    python manage.py migrate
} else {
    Write-Host "Файл manage.py не найден. Пропускаю миграции." -ForegroundColor Yellow
}

Write-Host "Все готово!" -ForegroundColor Green
