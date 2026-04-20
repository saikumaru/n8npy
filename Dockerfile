FROM python:3.13-alpine

RUN apk add --no-cache nodejs npm py3-scikit-learn && \
    npm install -g n8n

WORKDIR /app
COPY source/ .

EXPOSE 5678

CMD ["n8n", "start"]
