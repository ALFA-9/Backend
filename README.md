***

### Backend часть командного проекта в рамках Хакатона Яндекс Практикум Альфа-Банк "02.2024"

***

## Технологии:

[![Python](https://img.shields.io/badge/Python-%203.10-blue?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%204.2-blue?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DjangoRESTFramework-%203.14.0-blue?style=flat-square&logo=django)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-%205.3.6-blue?style=flat-square&logo=celery)](https://docs.celeryq.dev/en/stable/)
[![Redis](https://img.shields.io/badge/Redis-%205.0.1-blue?style=flat-square&logo=redis)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%2013-blue?style=flat-square&logo=PostgreSQL)]([https://www.postgresql.org/])
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.1.0-blue?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

[![Swagger](https://img.shields.io/badge/Swagger-%20?style=flat-square&logo=swagger)](https://swagger.io/)
[![Docker](https://img.shields.io/badge/Docker-%20?style=flat-square&logo=docker)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-%20?style=flat-square&logo=docsdotrs)](https://docs.docker.com/compose/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-%20?style=flat-square&logo=githubactions)](https://github.com/features/actions)
[![Nginx](https://img.shields.io/badge/Nginx-%20?style=flat-square&logo=nginx)](https://www.nginx.com/)
[![Certbot](https://img.shields.io/badge/certbot-%20?style=flat-square&logo=letsencrypt)](https://certbot.eff.org/)

***

## Функционал:

В процессе разработки проекта были реализованы:
- интуитивно понятный интерфейс
- удобное хранение и работа с записями в БД
- уведомления посредством отправки email

***

## Технические особенности:

Репозиторий включает в себя два файла **docker-compose.yml** и 
**docker-compose.production.yml**, что позволяет развернуть проект на
локальном или удалённом серверах.

Данная инструкция подразумевает, что на вашем локальном/удалённом сервере 
уже установлен Git, Python 3.10, пакетный менеджер pip, Docker, 
Docker Compose, утилита виртуального окружения python3-venv.

В проекте предусмотрена возможность запуска БД SQLite3 и PostgreSQL. Выбор 
БД осуществляется сменой значения CURRENT_DB на lite или postgre. 
lite = SQLite3, postgre = PostgreSQL.

В проекте настроена автодокументация с помощью **Swagger**. Для ознакомления 
перейдите по [ссылке](https://api.new.red-hand/api/docs/)

С подробными инструкциями запуска вы можете ознакомиться ниже.

***

## Как запустить:

### Запуск проекта в Docker-контейнерах с помощью Docker Compose:

Создайте и перейдите в директорию проекта:

```bash
mkdir alfa_backend
cd alfa_backend/
```

Скачайте и добавьте файл **docker-compose.production.yml** в директорию.

Cоздайте файл **.env**:

```bash
nano .env
```

Добавьте следующие строки и подставьте свои значения:
````dotenv
POSTGRES_DB=DB                   # название db
POSTGRES_USER=USER               # имя пользователя для db
POSTGRES_PASSWORD=PASSWORD       # пароль пользователя для db
DB_HOST=db                       # если поменять, то тогда нужно поменять название сервиса в docker-compose.production.yml
DB_PORT=5432                     # это порт для доступа к db
SECRET_KEY=SECRET_KEY            # SECRET_KEY в настройках django
DEBUG=False                      # True или False
ALLOWED_HOSTS=127.0.0.1 backend  # ваши адреса через пробел (пример:localhost 127.0.0.1 xxxx.com)
HOST_URL=http://localhost:8000   # ваш url адрес вместе с http/https
````

Установить docker: https://www.docker.com/get-started/

В терминале linux это можно сделать так:
````bash
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin 
````

Запустить Docker в директории с файлом **docker-compose.yaml** (чтобы запустить в фоновом режиме добавьте флаг -d):
````bash
docker compose up
````
В терминале Linux могут потребоваться права суперпользователя:
````bash
sudo docker compose up
````

Для доступа в админ-зону (если вам нужны какие-то данные из бд, или нужно создать объекты) перейдите на страницу http://localhost:8000/admin/:

Логин: `admin@admin.ru`

Пароль: `admin`

### Если вы хотите иметь возможность поменять код:

Склонируйте репозиторий:
````bash
git clone git@github.com:ALFA-9/Backend.git
````

Перейдите в папку Backend и запустите файл **docker-compose.yml**:
````bash
cd Backend
docker compose up
````

Для импорта начальных данных воспользуйтесь файлом **import.sh**:
````bash
sh import.sh
````

Если вы хотите прикрутить автоматизацию посредством GithubActions настройте файл **main.yml**

> **Примечание.** Любые изменения в коде при сохранении будут немедленно отображаться при запросах к серверу
***

## Авторы

[**Алексей Синюков**](https://github.com/aleksey2299-1)

[**Алексей Васильев**](https://github.com/aleksey-vasilev)

[**Денис Дриц**](https://github.com/Den2605)

[**Илья Симонов**](https://github.com/ilya-simonov)
