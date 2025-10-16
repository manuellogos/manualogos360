# Manual CMS - Wagtail

Un sistema de gestión de contenidos (CMS) basado en Wagtail para crear manuales de usuario con diseño minimalista y navegación jerárquica.

## Características

- 🎨 **Diseño minimalista** con sidebar de navegación
- 📚 **Estructura jerárquica**: Secciones > Subsecciones > Artículos  
- 🌍 **Multiidioma**: Español, Catalán, Gallego, Euskera, Inglés, Francés
- 🖼️ **Soporte completo de imágenes** con galerías
- 📝 **Editor rico** con bloques de contenido (texto, código, imágenes, alertas)
- 🔍 **Navegación automática** entre artículos (anterior/siguiente)
- 📱 **Responsive** con Bootstrap 5
- 🎨 **Syntax highlighting** para código con Prism.js

## Estructura del Proyecto

```
manual_cms/
├── manual/                     # App principal del manual
│   ├── models.py              # Modelos de páginas
│   ├── context_processors.py  # Procesadores de contexto
│   └── management/            # Comandos de gestión
├── manual_cms/                # Configuración del proyecto
│   ├── settings/              
│   │   ├── base.py           # Configuración base
│   │   ├── dev.py            # Configuración desarrollo
│   │   └── production.py     # Configuración producción
│   └── templates/
│       └── base.html         # Template base con navegación
└── static/                   # Archivos estáticos (CSS, JS)
```

## Instalación Local

1. **Crear entorno virtual**:
```bash
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**:
```bash
python manage.py migrate
```

4. **Configurar sitio inicial**:
```bash
python manage.py setup_site
```

5. **Recopilar archivos estáticos**:
```bash
python manage.py collectstatic
```

6. **Ejecutar servidor de desarrollo**:
```bash
python manage.py runserver
```

## Acceso

- **Sitio web**: http://localhost:8000
- **Panel de administración**: http://localhost:8000/admin
- **Usuario por defecto**: admin / admin123

## Despliegue

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas de despliegue en:
- Railway (recomendado)
- Render  
- DigitalOcean App Platform

## Uso

### Crear contenido

1. Accede al panel de administración (`/admin`)
2. Ve a "Páginas" en el menú
3. Crea la estructura:
   - **Manual Home Page**: Página principal
   - **Sección Page**: Secciones principales (ej: "Introducción")
   - **Subsección Page**: Subsecciones (ej: "Primeros pasos")
   - **Artículo Page**: Artículos individuales con contenido

### Estructura recomendada

```
📖 Manual de Usuario
├── 🏠 Introducción
│   ├── 📄 Primeros pasos
│   └── 📄 Requisitos del sistema
├── 🔧 Instalación
│   ├── 📄 Instalación en Windows
│   └── 📄 Instalación en Linux
└── 💡 Guías avanzadas
    ├── 📄 Configuración personalizada
    └── 📄 Solución de problemas
```

### Multiidioma

1. Ve a "Configuración" > "Locales"
2. Activa los idiomas necesarios  
3. Traduce el contenido usando el módulo Wagtail Localize

## Tecnologías

- **Backend**: Django 5.2, Wagtail 7.1
- **Frontend**: Bootstrap 5.3, Font Awesome 6.4
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Multiidioma**: wagtail-localize
- **Syntax Highlighting**: Prism.js

## Comandos Útiles

```bash
# Desarrollo
python manage.py runserver
python manage.py makemigrations
python manage.py migrate

# Configuración inicial
python manage.py setup_site

# Archivos estáticos
python manage.py collectstatic

# Traducciones
python manage.py makemessages -l es
python manage.py compilemessages
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.

## Soporte

Si tienes problemas:
1. Revisa la documentación en `/admin/`
2. Consulta los logs de la aplicación
3. Verifica las variables de entorno en producción

---

Desarrollado con ❤️ usando Wagtail