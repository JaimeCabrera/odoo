FROM odoo:17.0

# Instalar paquetes adicionales desde requirements.txt
COPY ./etc/requeriments.txt /tmp/requeriments.txt
RUN pip install --no-cache-dir -r /tmp/requeriments.txt
