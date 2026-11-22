FROM python:3.12-slim

# Usuario sin privilegios que ejecuta la API
RUN adduser --disabled-password --gecos '' api-user

WORKDIR /opt/api

# Dependencias (incluye el paquete del modelo en model-pkg/)
COPY requirements.txt /opt/api/
COPY model-pkg /opt/api/model-pkg
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Código de la API
COPY app /opt/api/app
COPY run.sh /opt/api/run.sh
RUN chmod +x /opt/api/run.sh && chown -R api-user:api-user /opt/api

USER api-user
ENV PORT=8001
EXPOSE 8001

CMD ["bash", "./run.sh"]
