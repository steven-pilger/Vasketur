 # BASE
 FROM python:3.7-slim AS base
 RUN apt-get update -qq
 RUN apt-get install -qq --force-yes curl gcc cron > /dev/null
 ENV PYTHONUNBUFFERED 1
 ENV PATH /root/.poetry/bin:${PATH}
 RUN mkdir /code
 WORKDIR /code
 ADD pyproject.toml /code/
 ADD poetry.lock /code/

 # DEVELOPMENT
 FROM base AS dev
 RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
 RUN poetry install
 ADD . /code/
 CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

 #PRODUCTION
 FROM dev AS production
 EXPOSE 8000
 CMD ["gunicorn", "-b", "0.0.0.0:8000", "vasketur.wsgi"]

 # CRON CONTAINER
 FROM dev AS cron
 RUN apt-get install -qq --force-yes cron > /dev/null
 COPY querystate-cron /etc/cron.d/querystate-cron
 RUN chmod 0600 /etc/cron.d/querystate-cron
 RUN crontab /etc/cron.d/querystate-cron
 CMD env > /.cronenv && cron -f
