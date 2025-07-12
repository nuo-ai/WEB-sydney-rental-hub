# Backend with Celery Integration

This document provides instructions for setting up and running the backend services, including the FastAPI application, Redis, and the Celery worker.

## 1. Prerequisites

- Python 3.8+
- Redis

### Installing Redis

**On macOS (using Homebrew):**
```bash
brew install redis
brew services start redis
```

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl enable redis-server.service
```

**On Windows:**
It is recommended to use the Windows Subsystem for Linux (WSL) to install and run Redis. Follow the Ubuntu/Debian instructions within your WSL environment.

**Using Docker (Recommended for all platforms):**
If you have Docker installed, you can easily run Redis in a container:
```bash
docker run -d -p 6379:6379 --name some-redis redis
```

To verify that Redis is running, you can use the `redis-cli`:
```bash
redis-cli ping
```
If it returns `PONG`, Redis is running correctly.

## 2. Environment Variables

Create a `.env` file in the project root directory (`WEB-sydney-rental-hub`) and add the following variables. Update the values to match your local setup.

```env
# Database Configuration
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port

# Redis Configuration
# If Redis is running on a different host or port, update this URL.
REDIS_URL=redis://localhost:6379/0

# API Security
API_KEY=your_secret_api_key
SECRET_KEY=a_very_secret_key_for_jwt
```

## 3. Running the Services

You need to run three separate processes in three different terminals from the project root directory (`WEB-sydney-rental-hub`).

### Terminal 1: Start the FastAPI Server

```bash
uvicorn backend.main:app --reload --port 8000
```
This will start the FastAPI application, which will be accessible at `http://localhost:8000`.

### Terminal 2: Start the Celery Worker

```bash
celery -A backend.celery_worker.celery_app worker --loglevel=info
```
This command starts the Celery worker, which will listen for and execute tasks from the Redis queue.

### Terminal 3: (Optional) Start the Celery Flower Monitoring Tool

Flower is a web-based tool for monitoring and administrating Celery clusters. It's highly recommended for development.

First, install it if you haven't:
```bash
pip install flower
```

Then, run it:
```bash
celery -A backend.celery_worker.celery_app flower --port=5555
```
You can then access the Flower dashboard at `http://localhost:5555`.

## 4. Testing the Integration

Once all services are running, you can test the Celery integration by sending requests to the task endpoints:

- **Trigger the debug task:**
  Send a `POST` request to `http://localhost:8000/api/tasks/debug` with your `X-API-Key` header.

- **Trigger the database task:**
  Send a `POST` request to `http://localhost:8000/api/tasks/db` with your `X-API-Key` header.

- **Check task status:**
  Send a `GET` request to `http://localhost:8000/api/tasks/{task_id}` (replace `{task_id}` with the ID you received from the previous requests) with your `X-API-Key` header.

You should see logs in your Celery worker terminal indicating that the tasks are being received and executed.
