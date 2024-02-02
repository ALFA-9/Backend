FROM python:3.10

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

# Добавляем строчку в requirements.txt в зависимости от DEBUG
ARG DEBUG
RUN if test "$(echo "$DEBUG" | tr '[:upper:]' '[:lower:]')" = "true"; then \
        echo "" >> requirements.txt; \
        echo "django-cors-headers==4.3.1" >> requirements.txt; \
    else \
        exit 1; \
    fi

RUN pip install -r requirements.txt --no-cache-dir

COPY . .