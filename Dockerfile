FROM python:3.9

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 8080
CMD ["python3", "db.py"]
CMD ["python3", "self.py"]
