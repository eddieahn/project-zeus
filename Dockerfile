
FROM python:3.13-slim-buster

WORKDIR /app

COPY ./Classification.py /app
COPY ./app.py /app

RUN pip install -r requirements.txt

ENV AZURE_OPENAI_API_KEY=de94456faa5b415b943034ed720811e
ENV AZURE_OPENAI_ENDPOINT=https://compasaoaiuks.openai.azure.com/
ENV AZURE_OPENAI_API_VERSION=2024-03-01-preview

# Expose the port where streamlit will run
EXPOSE 8501

# Run streamlit
ENTRYPOINT [ "streamlit", "run" ]
CMD ["app.py"]
