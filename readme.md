# Delivery Reporting System

**Описание:**
Приложение для просмотра отчетов о доставках. Состоит из двух частей:

* **Backend:** Django REST Framework (Python 3.12)
* **Frontend:** React + Vite (Node.js 20)

Подробное описание доступно на DeepWiki: [Delivery Reporting System](https://deepwiki.com/ferokuk/deliveries)

---

## 📁 Структура проекта

```
deliveries/
├── backend/            # Django backend (Python 3.12)
│   ├── deliveries_test_task/  # Django проект
│   ├── deliveries             # Основное приложение
│   ├── requirements.txt       # Список зависимостей
│   ├── Dockerfile            # Dockerfile для backend
│   ├── entrypoint.sh         # Скрипт запуска
│   ├── .env.example          # Пример переменных окружения
│   └── ...
├── frontend/           # React + Vite frontend (Node.js 20)
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile        # Dockerfile для frontend
│   ├── .env.example      # Пример переменных окружения
│   └── ...
├── docker-compose.yml   # Сборка и запуск всех сервисов
└── README.md            # Документация по проекту
```

---

## 🧰 Требования

* **Python 3.12**
* **Node.js 20**
* **PostgreSQL 15+**
* **Docker** и **Docker Compose** (для упрощенного запуска)

Если запускаешь без Docker, достаточно установить Python и Node.js требуемых версий.

---

## 🚀 Запуск локально

В проекте доступны два способа запуска: через Docker Compose (рекомендуется) и вручную.

### 1. Через Docker Compose (рекомендуется)

1. **Клонируй репозиторий и перейди в корень проекта:**

   ```bash
   git clone https://github.com/ferokuk/deliveries.git
   cd deliveries
   ```

2. **Скопируй примеры переменных окружения:**

   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

   Отредактируй `backend/.env` и `frontend/.env` указав параметры БД.

3. **Запусти сборку и поднимите сервисы:**

   ```bash
   docker-compose up --build
   ```

4. **Открой браузер и перейди по адресам:**

   * Frontend: [http://localhost:3000](http://localhost:3000)
   * Backend API (Django): [http://localhost:8000](http://localhost:8000)

Все миграции и первоначальные настройки базы данных выполняются автоматически через `entrypoint.sh` внутри контейнера backend.

---

### 2. Вручную (без Docker)

#### Backend (Django REST Framework)

1. Перейди в папку `backend/` и создай виртуальное окружение:

   ```bash
   cd backend
   python3.12 -m venv venv
   source venv/bin/activate      # Windows: venv\\Scripts\\activate
   ```

2. Установи зависимости и создайте файл переменных окружения:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   cp .env.example .env
   ```

   Отредактируй `.env`, если нужно.

3. Выполни миграции и запусти сервер:

   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

   Backend будет доступен по адресу [http://localhost:8000](http://localhost:8000).

#### Frontend (React + Vite)

1. Перейди в папку `frontend/`:

   ```bash
   cd frontend
   ```

2. Установи зависимости и создай файл окружения:

   ```bash
   npm install
   cp .env.example .env
   ```

   Убедись, что в `.env` указан правильный `VITE_API_BASE_URL` (по умолчанию `http://127.0.0.1:8000`).

3. Запусти режим разработки:

   ```bash
   npm run dev -- --host 0.0.0.0 --port 3000
   ```

   Frontend будет доступен по адресу [http://localhost:3000](http://localhost:3000).

---

## 🔐 Переменные окружения

Примеры файлов `.env.example` находятся в папках `backend/` и `frontend/`. Скопируй их и переименуй в `.env`.

### backend/.env.example

```env
SECRET_KEY=your_django_secret_key_here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=deliverydb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1111
POSTGRES_HOST=db
REACT_ORIGIN=http://localhost:3000
DJANGO_ORIGIN=http://localhost:8000
```

### frontend/.env.example

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## ⛑️ Отладка

* Проверь, что порты 3000 (frontend) и 8000 (backend) свободны.
* В случае проблем с подключением к базе PostgreSQL (при Docker) проверь, что сервис `db` поднялся и прошел healthcheck.

---

