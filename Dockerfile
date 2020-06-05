FROM registry.redhat.io/ubi8/python-38

COPY requirements.txt app.py /

RUN pip install -r /requirements.txt

ENTRYPOINT ["python", "/app.py"]
