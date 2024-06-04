FROM python:3
LABEL authors="v-akgusain"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5432
EXPOSE 8084

CMD [ "python", "LEISearchWithFlask.py" ]
