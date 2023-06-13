FROM tiangolo/uwsgi-nginx:python3.7
RUN set -x \
    && apt-get update && apt-get install apt-utils --no-install-recommends --no-install-suggests -y redis-server libssl-dev

WORKDIR /app
COPY requirements.txt   /app/requirements.txt
COPY sql                /app/socrates-osticket-billing/sql
COPY static             /app/static
COPY templates          /app/templates
COPY datamodel.py       /app/datamodel.py
COPY main.py            /app/main.py
COPY prestart.sh        /app/prestart.sh
COPY uwsgi.ini          /app/uwsgi.ini
RUN pip3 install -r     /app/requirements.txt

