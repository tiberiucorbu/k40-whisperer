FROM python:2.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk add --no-cache gcc libxml2-dev libxslt-dev libc-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./build.py" ]
