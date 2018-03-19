FROM python:3.6.4-slim

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENV FLASK_APP=run.py
EXPOSE 80

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]
