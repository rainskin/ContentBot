FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install
COPY . .
ENV TZ="Europe/Moscow"
CMD poetry run python src