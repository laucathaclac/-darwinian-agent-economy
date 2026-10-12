FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DAE_HOST=0.0.0.0
WORKDIR /app
COPY . .
RUN python -m pip install --no-cache-dir -e .
EXPOSE 8787
CMD ["python", "scripts/dae_health_sentinel_server.py"]
