FROM python:3.7-alpine

WORKDIR /usr/src/app

RUN addgroup -S lasercutter  && adduser -S -G lasercutter lasercutter

COPY requirements.txt ./

RUN apk add --no-cache gcc libxml2-dev libxslt-dev libc-dev \
                       # Pillow dependencies
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python setup.py py2exe
RUN python -m unittest discover -s ./ -p 'test_*.py'

CMD [ "python", "./k40_wishperer.py" ]
