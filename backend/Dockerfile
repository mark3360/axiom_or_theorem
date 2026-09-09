FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y curl git python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN curl https://elan.lean-lang.org/elan-init.sh -sSf | \
    sh -s -- -y --default-toolchain stable

ENV PATH="/root/.elan/bin:${PATH}"

RUN elan toolchain install stable

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
