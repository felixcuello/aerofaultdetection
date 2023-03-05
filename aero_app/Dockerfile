FROM python:3.10.4-bullseye

COPY . /app

#  Dependencias de python
# ------------------------------------------------------
WORKDIR /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
ENV FLASK_APP=run.py
CMD echo "This worked"
