
FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y g++ dumb-init libev-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /usr
RUN pip install "poetry==1.1.12"
COPY pyproject.toml poetry.lock ${WORKDIR}/
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o ${WORKDIR}/requirements.txt
RUN pip install --force-reinstall --no-cache-dir -r ${WORKDIR}/requirements.txt

COPY . /usr
RUN pip install .

EXPOSE 5000

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["python3", "src/webapp/run.py"]