FROM python:3.13-slim

WORKDIR /app
COPY fetcher.py redirector.py internal.py ./

EXPOSE 80
CMD ["python", "fetcher.py"]
