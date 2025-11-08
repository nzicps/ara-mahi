FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PORT=8080
CMD ["gunicorn", "src.web.app:app", "--bind", "0.0.0.0:8080"]
