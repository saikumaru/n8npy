FROM python:3.13-alpine

RUN apk add --no-cache nodejs npm gcc musl-dev && \
    npm install -g n8n && \
    pip install --no-cache-dir scikit-learn

WORKDIR /app
COPY source/ .

EXPOSE 5678

CMD ["n8n", "start"]
