FROM registry.gitlab.com/chariot-h2020/iot-modeling-language

VOLUME ["/workspace"]
WORKDIR /workspace

COPY . .

RUN apt-get update && apt-get install -y libgmp-dev python-dev gnupg gcc g++ make libffi-dev
RUN pip install -U pip && pip install -r requirements_dev.txt && pip install pytest && pip install gunicorn
RUN python setup.py install

CMD ["python3"]