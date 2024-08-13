## Quickstart

### 1. Clone repository
```bash
git clone <repo URL>
cd fast-api-boilerplate
```

### 2. Setup postgres using docker compose.
```bash
docker-compose up -d
```

### 3. Install dependecies using pip
```bash
pip install -r ./requirements.txt
```

### 4. Run Alembic migrations
```bash
alembic upgrade head
```

### 5. Run app
```bash
uvicorn app.main:app --reload
or
python main.py
```

## License

The code is under MIT License.
