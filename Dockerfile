FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin netcat-openbsd

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]