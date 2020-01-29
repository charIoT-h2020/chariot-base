FROM registry.gitlab.com/chariot-h2020/iot-modeling-language

VOLUME ["/workspace"]
WORKDIR /workspace

COPY . .

RUN apk add gnupg gcc g++ make python3-dev libffi-dev openssl-dev gmp-dev
RUN pip install -r requirements_dev.txt
RUN python setup.py install

CMD ["python3"]