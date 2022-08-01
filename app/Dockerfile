FROM python:3.8.2-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
ENV APP_HOME=/usr/src/app

RUN mkdir $APP_HOME/staticfiles && \
    mkdir $APP_HOME/mediafiles

COPY ./Pipfile /usr/src/app
COPY ./Pipfile.lock /usr/src/app

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --system
    
COPY . $APP_HOME
COPY ./entrypoint.sh $APP_HOME

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]