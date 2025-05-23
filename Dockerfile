FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY . .
# Instalar dependencias necesarias
RUN pip install requests

# Cambiar puerto expuesto (aunque este script no tiene servidor web, lo dejamos preparado)
EXPOSE 9999

# Comando para ejecutar el script
CMD ["python", "graphhopper.py"]

