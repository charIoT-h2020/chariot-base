FROM registry.gitlab.com/chariot-h2020/iot-modeling-language AS builder

WORKDIR /workspace
COPY . .

RUN apk add gnupg gcc g++ make python3-dev libffi-dev openssl-dev gmp-dev
RUN pip install -U pip && pip install -r requirements_dev.txt && pip install pytest && pip install gunicorn
RUN python setup.py install

FROM python:3.7-alpine AS final
COPY --from=builder /usr/local/lib/python3.7 /usr/local/lib/python3.7
CMD ["python3"]