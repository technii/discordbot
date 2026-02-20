FROM python:3.14-slim
WORKDIR /app
COPY main.py /app/
COPY token.json /app/
COPY sounds /app/
COPY images /app/
COPY requirements.txt /app/
RUN pip install --upgrade & pip install -r requirements.txt
CMD ["python", "main.py"]
