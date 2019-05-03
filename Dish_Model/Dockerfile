FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN FLASK_APP=app.py
RUN DISH_MODEL=train.py
COPY app.py ./

CMD ["flask", "run", "--host=0.0.0.0"]
