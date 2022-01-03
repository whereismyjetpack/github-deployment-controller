FROM python:3.8.5-slim-buster

WORKDIR /app

RUN useradd -m app

# Trivy security findings
RUN apt-get update && apt-get install -y \ 
  libgcrypt20 \ 
  libgnutls30=3.6.7-4+deb10u7 \
  libhogweed4=3.4.1-1+deb10u1 \ 
  liblz4-1=1.8.3-1+deb10u1 \ 
  libnettle6=3.4.1-1+deb10u1 \ 
  libp11-kit0 \ 
  libsqlite3-0 \
  libssl1.1=1.1.1d-0+deb10u7 \
  libsystemd0 \ 
  apt \
  libudev1 \
  libzstd1 \
  openssl=1.1.1d-0+deb10u7 &&  \
  rm -rf /var/lib/apt/lists*
  
  
RUN pip install -U pip
RUN pip install poetry
COPY --chown=app pyproject.toml poetry.lock /app/
USER app
RUN poetry config virtualenvs.create false
ENV PIP_USER=yes
ENV PATH=$PATH:/home/app/.local/bin
RUN poetry install
COPY --chown=app . /app

CMD ["kopf", "run", "-A",  "lib/run.py", "--log-format=json"]
