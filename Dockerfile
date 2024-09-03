FROM python:3.8.10-slim
<<<<<<< HEAD

ENV PYTHONUNBUFFERED=1
ENV PORT=8000
#ENV DATABASE_URL=mysql+pymysql://remittance:remittance2024@10.11.12.111/remittance_test

WORKDIR /app

RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    libmariadb-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_latest.txt .
RUN pip install --no-cache-dir -r requirements_latest.txt

COPY pyproject.toml poetry.lock* /app/

# Install pip and Poetry
RUN pip install --upgrade pip && \
    pip install poetry==1.8.3

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . /app/
COPY alembic.sh /app/
RUN chmod +x /app/alembic.sh

EXPOSE 8000
CMD ["/app/alembic.sh"]
=======
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
>>>>>>> 4ff072eea4bf3d9e21bdfa50534e18dd866d673d
