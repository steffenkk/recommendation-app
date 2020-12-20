FROM python:3.7-slim

WORKDIR /home/app

ADD data /home/app/data
ADD src  /home/app/src
ADD conf /home/app/conf

COPY setup.py .
COPY requirements.txt .
COPY README.md .
RUN python3.7 -m pip install --upgrade pip && python3.7 -m pip install . && python3.7 -m pip install -r requirements.txt

# run console script for data prep
RUN prep

EXPOSE 8083

CMD uvicorn main:app --app-dir ./src --host 0.0.0.0 --port 8083 --reload