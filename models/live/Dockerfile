FROM continuumio/anaconda3
COPY ./model_flask /usr/local/python/
EXPOSE 8000
RUN apt-get update && apt-get install -y apache2 \
    apache2-dev \
    nano \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /var/www/models_api/
COPY ./models_api.wsgi /var/www/models_api/models_api.wsgi
COPY ./model_flask /var/www/models_api/
RUN pip install -r requirements.txt
RUN /opt/conda/bin/mod_wsgi-express install-module
RUN mod_wsgi-express setup-server models_api.wsgi --port=8000 \
    --user www-data --group www-data \
    --server-root=/etc/mod_wsgi-express-80
CMD /etc/mod_wsgi-express-80/apachectl start -D FOREGROUND