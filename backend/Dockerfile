FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*

RUN curl https://elan.lean-lang.org/elan-init.sh -sSf | \
    sh -s -- -y --default-toolchain stable

ENV PATH="/root/.elan/bin:${PATH}"

# Explicitly install the Lean toolchain during image creation
RUN elan toolchain install stable

WORKDIR /lean