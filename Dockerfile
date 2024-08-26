FROM python:3.8.10-slim
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV DATABASE_URL=mysql+pymysql://remit_admin:remit_admin@127.0.0.1/remit
WORKDIR /app
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmysqlclient-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY requirements_latest.txt .
RUN pip install --no-cache-dir -r requirements_latest.txt
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-dev --no-interaction --no-ansi
COPY . /app/
RUN poetry run alembic -c /app/project/alembic.ini upgrade head
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8000"]