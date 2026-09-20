FROM python:3.13-slim
WORKDIR /app
COPY gateway.py callback.py .
RUN mkdir -p /shared
EXPOSE 80
CMD ["python", "gateway.py"]
