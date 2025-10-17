#!/usr/bin/env bash
# Build script para Render

set -o errexit  # Salir si hay errores

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "📁 Creando directorio de archivos estáticos..."
mkdir -p staticfiles

echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

echo "👤 Configurando usuario admin..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@localhost', 'admin123');
    print('✅ Superusuario admin creado');
else:
    print('⚠️  Superusuario admin ya existe');
" || echo "Error creando superusuario, continuando..."

echo "🎉 Build completado exitosamente"