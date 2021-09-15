FROM python:3.8.5-slim-buster

WORKDIR /app

RUN useradd -m app

# Trivy security findings
RUN apt-get update && apt-get install -y \ 
  libgcrypt20 \ 
  libgnutls30 \
  libhogweed4 \ 
  liblz4-1 \ 
  libnettle6 \ 
  libp11-kit0 \ 
  libsqlite3-0 \
  libssl1.1 \
  libsystemd0 \ 
  apt \
  libudev1 \
  libzstd1 \
  openssl &&  \
  rm -rf /var/lib/apt/lists*
  
  

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY --chown=app pyproject.toml poetry.lock /app/
RUN poetry install
USER app
COPY --chown=app . /app

CMD ["kopf", "run", "lib/run.py"]
