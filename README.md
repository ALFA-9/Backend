## Backend часть

### Как запустить:

Скопировать код к себе:
````
git clone git@github.com:ALFA-9/Backend.git
````

Установить docker: https://www.docker.com/get-started/

В терминале linux это можно сделать так:
````
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin 
````

В директории проекта создайте файл .env c данными:
````
POSTGRES_DB=<название db>
POSTGRES_USER=<имя пользователя для db>
POSTGRES_PASSWORD=<пароль пользователя для db>
DB_HOST=db # если поменять, то тогда нужно поменять название сервиса в docker-compose.production.yml
DB_PORT=5432 # это порт по умолчанию для db
SECRET_KEY=<SECRET_KEY в настройках django>
DEBUG=<True или False>
ALLOWED_HOSTS=<ваши адреса через пробел (пример:localhost 127.0.0.1 xxxx.com)>
````


Запустить Docker в директории с файлом (чтобы запустить в фоновом режиме добавьте флаг -d):
````
docker-compose up
````
В терминале Linux могут потребоваться права суперпользователя:
````
sudo docker-compose up
````
### Как начать?

Перейти по адресу localhost:8000/

### Доступ по Api

__Вся информация касательно api доступна на странице localhost:8800/api/docs/:__

### Как запустить вместе с фронтом:

Проделать все предыдущие шаги.

Скопировать код frontend'а в папку с backend'ом:
````
git clone git@github.com:ALFA-9/Frontend.git
````

Добавить в папку frontend'a файл Dockerfile с содержимым:
````
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
RUN npm install --global http-server

CMD ["npx", "-y", "http-server", "-p", "8000", "/app/build"]
````

Добавить в файл docker-compose.yaml в блок service следующие сроки:
````
  frontend:
    env_file: .env
    build: ./frontend/
    command: cp -r /app/build/. /frontend_static/
    volumes:
      - static:/frontend_static
````
