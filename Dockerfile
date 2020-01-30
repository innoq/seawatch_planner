FROM python:3-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN \
 apk add --no-cache postgresql-libs gettext && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
COPY . /app/

# collect static files
RUN python manage.py collectstatic --noinput

# Generate translations
RUN django-admin compilemessages