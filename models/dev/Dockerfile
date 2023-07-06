FROM continuumio/anaconda3
COPY ./model_flask /usr/local/python/
EXPOSE 5000
WORKDIR /usr/local/python/
RUN pip install -r requirements.txt
CMD python models_api.py