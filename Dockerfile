FROM python:3.10-slim

WORKDIR /action/workspace
COPY requirements.txt *.py /action/workspace/


RUN apt-get -y update \
    && apt-get -y install --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["/action/workspace/src/ot_analyze.py"]
ENTRYPOINT ["python3", "-u"]