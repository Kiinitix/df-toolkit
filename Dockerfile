FROM python:3.11-slim-buster

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "./Insight/main.py"]