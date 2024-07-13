## Quickstart

### 1. Install dependecies with [Poetry](https://python-poetry.org/docs/)

```bash
cd your_project_name

### Poetry install (python3.12)
poetry install
```

### 2. Setup database and migrations

```bash
### Setup database
docker-compose up -d

### Run Alembic migrations
alembic upgrade head
```

### 3. Run app

```bash
uvicorn app.main:app --reload
```

<br>

### 3. Create request and response schemas

There are only 2 files: `requests.py` and `responses.py` in `schemas` folder and I would keep it that way even for few dozen of endpoints. Not to mention this is opinionated.

```python
# app/schemas/requests.py

(...)


class PetCreateRequest(BaseRequest):
    pet_name: str

```

```python
# app/schemas/responses.py

(...)


class PetResponse(BaseResponse):
    id: int
    pet_name: str
    user_id: str

```

<br>

## License

The code is under MIT License.