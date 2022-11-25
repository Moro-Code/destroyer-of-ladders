FROM python:3.8-alpine

# install dependencies 
RUN apk add --no-cache gcc libffi-dev musl-dev linux-headers g++

# install poetry on image
RUN pip install "poetry==1.2.2"

# copy the dependency files 
COPY poetry.lock pyproject.toml ./

# install production dependencies
RUN POETRY_VIRTUALENVS_CREATE=false \
&& poetry install --no-dev --no-interaction --no-ansi


# set the working directory where the app will be copied
WORKDIR /usr/app/src

COPY ./models /usr/app/src/models
COPY main.py /usr/app/src/main.py
COPY server.py /usr/app/src/server.py


EXPOSE 8000
CMD poetry run python main.py