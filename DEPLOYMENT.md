# Guía de Despliegue - Manual CMS Wagtail

## Preparación del Proyecto

Tu proyecto ya está configurado para producción con:
- ✅ Settings de producción (`production.py`)
- ✅ Dependencias actualizadas (`requirements.txt`)
- ✅ Configuración de proceso (`Procfile`)
- ✅ Versión de Python (`runtime.txt`)
- ✅ Archivo `.gitignore`

## Opciones de Hosting Recomendadas

### 1. Railway (RECOMENDADO)
**Ventajas:** Fácil despliegue, base de datos PostgreSQL gratis, SSL automático

### 2. Render
**Ventajas:** Plan gratuito generoso, fácil configuración

### 3. DigitalOcean App Platform
**Ventajas:** $5/mes, muy estable, fácil escalabilidad

---

## OPCIÓN 1: Despliegue en Railway

### Paso 1: Preparar el repositorio
```bash
# Inicializar git (si no lo has hecho)
git init
git add .
git commit -m "Initial commit - Manual CMS"

# Subir a GitHub (crear repositorio en github.com primero)
git remote add origin https://github.com/TU_USUARIO/manual-cms.git
git push -u origin main
```

### Paso 2: Configurar en Railway
1. Ve a [railway.app](https://railway.app)
2. Registrate con GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detectará automáticamente que es Django

### Paso 3: Configurar base de datos
1. En el dashboard del proyecto, click "Add Service" → "PostgreSQL"
2. Railway creará automáticamente la variable `DATABASE_URL`

### Paso 4: Configurar variables de entorno
En el dashboard → Settings → Environment → Add Variable:

```
DJANGO_SETTINGS_MODULE=manual_cms.settings.production
SECRET_KEY=tu-clave-secreta-muy-larga-y-compleja-aqui
PYTHONPATH=/app
```

### Paso 5: Configurar dominio personalizado (opcional)
1. Settings → Custom Domain
2. Añadir tu dominio

---

## OPCIÓN 2: Despliegue en Render

### Paso 1: Crear archivo `build.sh`
```bash
#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
"
```

### Paso 2: Configurar en Render
1. Ve a [render.com](https://render.com)
2. "New" → "Web Service"
3. Conecta tu repositorio GitHub
4. Configuración:
   - **Environment:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn manual_cms.wsgi:application`

### Paso 3: Variables de entorno
```
DJANGO_SETTINGS_MODULE=manual_cms.settings.production
SECRET_KEY=tu-clave-secreta-muy-larga-y-compleja-aqui
DATABASE_URL=postgresql://[automatico]
```

---

## OPCIÓN 3: DigitalOcean App Platform

### Paso 1: Crear `app.yaml`
```yaml
name: manual-cms
services:
- name: web
  source_dir: /
  github:
    repo: TU_USUARIO/manual-cms
    branch: main
  run_command: gunicorn manual_cms.wsgi:application
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DJANGO_SETTINGS_MODULE
    value: manual_cms.settings.production
  - key: SECRET_KEY
    value: tu-clave-secreta
databases:
- name: manual-db
  engine: PG
  size: db-s-dev-database
```

---

## Post-Despliegue

### 1. Crear superusuario
Ejecuta en la terminal de tu hosting:
```bash
python manage.py createsuperuser
```

### 2. Configurar sitio Wagtail
1. Ve a `/admin/sites/`
2. Edita el sitio por defecto
3. Cambia el hostname por tu dominio
4. Selecciona tu HomePage como página raíz

### 3. Configurar idiomas
1. Ve a `/admin/wagtaillocalize/locale/`
2. Activa los idiomas que necesites

---

## Solución de Problemas Comunes

### Error de archivos estáticos
Si no se cargan CSS/JS:
```bash
python manage.py collectstatic --noinput
```

### Error de base de datos
```bash
python manage.py migrate
```

### Error 500
Revisa los logs en tu plataforma de hosting y verifica:
- Variables de entorno correctas
- SECRET_KEY configurado
- ALLOWED_HOSTS incluye tu dominio

---

## Mantenimiento

### Actualizaciones
```bash
git add .
git commit -m "Descripción del cambio"
git push
```

El hosting se actualizará automáticamente.

### Backups
- Railway: Backups automáticos de BD
- Render: Configurar backups manuales
- DigitalOcean: Backups automáticos disponibles

---

## ¿Qué opción elegir?

**Para empezar rápido:** Railway
**Para proyectos profesionales:** DigitalOcean
**Para presupuesto ajustado:** Render (plan gratuito)

## Próximos pasos recomendados

1. Elegir plataforma de hosting
2. Configurar repositorio Git
3. Seguir la guía de la plataforma elegida
4. Configurar dominio personalizado
5. Añadir contenido al manual

¿Qué plataforma prefieres? Te puedo ayudar con el proceso específico.