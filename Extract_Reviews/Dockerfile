FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY emerald_reviews.json ./
COPY extract_reviews.py ./app.py

CMD ["python3", "app.py"]
