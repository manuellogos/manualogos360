#!/usr/bin/env bash
# Build script para Render

set -o errexit  # Salir si hay errores

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate

# Configurar sitio con comando personalizado
python manage.py setup_site