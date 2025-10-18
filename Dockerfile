# Python 3.11 slim para menor tamaño
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY src/ ./src/
COPY docs/ ./docs/

# Puerto de la API
EXPOSE 8001

# Variables de entorno: logs sin buffer + nivel ERROR por defecto
ENV PYTHONUNBUFFERED=1 \
    LOG_LEVEL=ERROR

# Ejecutar con uvicorn
CMD ["uvicorn", "src.portfolio.api:app", "--host", "0.0.0.0", "--port", "8001"]
