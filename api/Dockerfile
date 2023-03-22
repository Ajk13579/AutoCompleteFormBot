FROM joyzoursky/python-chromedriver:3.9-alpine

WORKDIR /usr/src/app
#COPY poetry.lock pyproject.toml /usr/src/app/

#RUN pip3 install poetry
#RUN poetry ins/tall

COPY requirements.txt /usr/src/app/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /usr/src/app

#CMD ["poetry", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]