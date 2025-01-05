FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8501

CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python data/data_processing.py && \
    python manage.py load_data data/cleaned_data/ && \
    streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501
