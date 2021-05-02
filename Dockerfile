FROM python:3.7.5-slim-buster
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY . /src
CMD [ "python", "/src/run.py" ]