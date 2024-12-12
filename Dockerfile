FROM odoo:17.0

# Instalar paquetes adicionales desde requirements.txt
COPY ./etc/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
