FROM python:3.12-slim AS mosaic-base

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

#Download the CIFAR-10 dataset
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN curl https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz | tar -xz -C /app

COPY ./*.py /app/
COPY ./nearest_neighbour /app/nearest_neighbour

FROM mosaic-base AS mosaic

ARG NUM_POINTS=5000
ENV NUM_POINTS=${NUM_POINTS}

RUN python3 create_algos.py $NUM_POINTS

CMD ["python", "app.py"]