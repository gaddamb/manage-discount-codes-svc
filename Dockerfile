FROM python:3.10
COPY requirements.txt .
WORKDIR /usr/src/app
COPY . .
RUN python3 -m pip install -r \
    requirements.txt --quiet --no-cache-dir \
    && rm -f requirements.txt

CMD [ "python", "./main.py" ]