FROM tensorflow/tensorflow:latest-py3

LABEL maintainer="sri.protege@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /deeplearn_ui/requirements.txt

WORKDIR /deeplearn_ui
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /deeplearn_ui

ENTRYPOINT [ "python3" ]

CMD [ "deeplearn_io/deeplearn_api.py" ]