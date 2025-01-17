
FROM python:3.8-slim-buster

WORKDIR /app

ADD ./ingestion /app/ingestion
ADD ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install jupyter

ENV AZURE_OPENAI_API_KEY=
ENV AZURE_OPENAI_ENDPOINT=https://compasaoaiuks.openai.azure.com/
ENV AZURE_OPENAI_API_VERSION=2024-03-01-preview

# Expose the port where gunicorn and jupyter will run
EXPOSE 80 2323

# Run the gunicorn server and the jupyter notebook
CMD gunicorn -b 0.0.0.0:80 ingestion:app & jupyter notebook --ip='*' --port=2323 --no-browser --allow-root
