FROM python:3.12-slim

# Usuario sin privilegios que ejecuta el tablero
RUN adduser --disabled-password --gecos '' dash-user

WORKDIR /opt/app/dashboard

COPY dashboard/requirements.txt /opt/app/dashboard/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Código del tablero y resúmenes que lee datos.py (../reports/exploracion)
COPY dashboard/ /opt/app/dashboard/
COPY reports/exploracion/ /opt/app/reports/exploracion/
RUN chown -R dash-user:dash-user /opt/app

USER dash-user
# URL de la API de predicción (se puede cambiar al lanzar el contenedor con -e API_URL=...)
ENV PORT=8050 \
    API_URL=http://localhost:8001
EXPOSE 8050

CMD ["sh", "-c", "gunicorn app:server -b 0.0.0.0:${PORT} --workers 1 --timeout 120"]