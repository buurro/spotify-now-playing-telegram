FROM python:3.7.5-slim-buster
COPY . /src
RUN pip install -r /src/requirements.txt
CMD [ "python", "/src/run.py" ]