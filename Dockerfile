FROM python:2.7-alpine

WORKDIR /usr/src/app

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

CMD [ "python", "./test.py" ]
