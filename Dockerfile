FROM python:3.7.3-slim-stretch

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY main.py .

ENTRYPOINT [ "python", "./main.py" ]
