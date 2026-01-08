FROM python:3.11-alpine


# Устанавливаем рабочую директорию в контейнере
WORKDIR /usr/src/core

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Копируем файл зависимостей и устанавливаем их
COPY req.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r req.txt

# Копируем исходный код проекта
COPY . .

# Собираем статические файлы
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]

# Устанавливаем Nginx

# Копируем конфигурацию Nginx



# Открываем порт 80
EXPOSE 80
EXPOSE 8000

#nginx &&

# Запускаем Nginx и Gunicorn
CMD ["sh", "-c", " exec gunicorn config.wsgi:application --bind 0.0.0.0:8000"]


