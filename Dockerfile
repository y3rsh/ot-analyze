FROM python:3.10-slim
LABEL org.opencontainers.image.source https://github.com/y3rsh/ot-analyze

WORKDIR /action/workspace
COPY requirements.txt *.py /action/workspace/

RUN python3 -m pip install --no-cache-dir -r requirements.txt \
    && apt-get -y update \
    && apt-get -y install --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

CMD ["/action/workspace/ot_analyze.py"]
ENTRYPOINT ["python3", "-u"]