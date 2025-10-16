from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from home.models import HomePage
from manual.models import (ArticuloPage, ManualHomePage, SeccionPage,
                           SubseccionPage)


class Command(BaseCommand):
    help = 'Inicializa el manual con contenido de ejemplo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando estructura del manual...'))

        try:
            # Obtener o crear la página raíz
            site = Site.objects.get(is_default_site=True)
            root_page = site.root_page

            # Verificar si ya existe una página del manual
            existing_manual = ManualHomePage.objects.first()
            if existing_manual:
                self.stdout.write(self.style.WARNING('El manual ya existe. Saltando creación.'))
                return

            # Crear página principal del manual
            manual_home = ManualHomePage(
                title="Manual de Usuario - Logos360",
                intro="<p>Bienvenido al manual de usuario de Logos360. Aquí encontrarás toda la información necesaria para utilizar la plataforma de manera eficiente.</p>",
                slug="manual",
            )
            root_page.add_child(instance=manual_home)
            manual_home.save_revision().publish()

            # Crear sección "Primeros Pasos"
            seccion_primeros_pasos = SeccionPage(
                title="Primeros Pasos",
                descripcion="<p>Todo lo que necesitas saber para empezar a usar Logos360.</p>",
                icono="fa-rocket",
                slug="primeros-pasos",
            )
            manual_home.add_child(instance=seccion_primeros_pasos)
            seccion_primeros_pasos.save_revision().publish()

            # Artículo: Introducción
            articulo_intro = ArticuloPage(
                title="Introducción a Logos360",
                slug="introduccion",
                contenido=[
                    {
                        'type': 'parrafo',
                        'value': '<p>Logos360 es una plataforma integral diseñada para simplificar la gestión de tu negocio. En este manual aprenderás a utilizar todas sus funcionalidades.</p>'
                    },
                    {
                        'type': 'alerta',
                        'value': {
                            'tipo': 'info',
                            'titulo': 'Tip importante',
                            'contenido': '<p>Te recomendamos leer este manual paso a paso para aprovechar al máximo la plataforma.</p>'
                        }
                    }
                ]
            )
            seccion_primeros_pasos.add_child(instance=articulo_intro)
            articulo_intro.save_revision().publish()

            # Artículo: Registro y Login
            articulo_login = ArticuloPage(
                title="Registro y Acceso",
                slug="registro-acceso",
                contenido=[
                    {
                        'type': 'parrafo',
                        'value': '<h3>Cómo registrarse</h3><p>Para registrarte en Logos360, sigue estos pasos:</p><ol><li>Ve a la página de registro</li><li>Completa el formulario con tus datos</li><li>Verifica tu email</li><li>¡Listo! Ya puedes acceder</li></ol>'
                    },
                    {
                        'type': 'codigo',
                        'value': {
                            'lenguaje': 'bash',
                            'codigo': '# Ejemplo de configuración inicial\ncp .env.example .env\nnpm install\nnpm start'
                        }
                    }
                ]
            )
            seccion_primeros_pasos.add_child(instance=articulo_login)
            articulo_login.save_revision().publish()

            # Crear sección "Configuración"
            seccion_config = SeccionPage(
                title="Configuración",
                descripcion="<p>Aprende a configurar tu cuenta y personalizar la plataforma.</p>",
                icono="fa-cog",
                slug="configuracion",
            )
            manual_home.add_child(instance=seccion_config)
            seccion_config.save_revision().publish()

            # Subsección: Configuración de Cuenta
            subseccion_cuenta = SubseccionPage(
                title="Configuración de Cuenta",
                descripcion="<p>Personaliza tu perfil y ajustes de cuenta.</p>",
                slug="configuracion-cuenta",
            )
            seccion_config.add_child(instance=subseccion_cuenta)
            subseccion_cuenta.save_revision().publish()

            # Artículo: Perfil de Usuario
            articulo_perfil = ArticuloPage(
                title="Editar Perfil de Usuario",
                slug="editar-perfil",
                contenido=[
                    {
                        'type': 'parrafo',
                        'value': '<p>Desde tu perfil puedes actualizar tu información personal y preferencias.</p>'
                    },
                    {
                        'type': 'alerta',
                        'value': {
                            'tipo': 'warning',
                            'titulo': 'Importante',
                            'contenido': '<p>Asegúrate de mantener tu información de contacto actualizada.</p>'
                        }
                    }
                ]
            )
            subseccion_cuenta.add_child(instance=articulo_perfil)
            articulo_perfil.save_revision().publish()

            # Crear sección "API y Desarrolladores"
            seccion_api = SeccionPage(
                title="API y Desarrolladores",
                descripcion="<p>Documentación técnica para desarrolladores.</p>",
                icono="fa-code",
                slug="api-desarrolladores",
            )
            manual_home.add_child(instance=seccion_api)
            seccion_api.save_revision().publish()

            # Artículo: Autenticación API
            articulo_api_auth = ArticuloPage(
                title="Autenticación de la API",
                slug="api-autenticacion",
                contenido=[
                    {
                        'type': 'parrafo',
                        'value': '<p>La API de Logos360 utiliza autenticación basada en tokens JWT.</p>'
                    },
                    {
                        'type': 'codigo',
                        'value': {
                            'lenguaje': 'javascript',
                            'codigo': '// Ejemplo de autenticación\nconst token = await fetch("/api/auth/login", {\n  method: "POST",\n  headers: {\n    "Content-Type": "application/json"\n  },\n  body: JSON.stringify({\n    email: "usuario@example.com",\n    password: "password123"\n  })\n});'
                        }
                    },
                    {
                        'type': 'alerta',
                        'value': {
                            'tipo': 'error',
                            'titulo': 'Seguridad',
                            'contenido': '<p>Nunca compartas tu token de API. Manténlo seguro y rotalo regularmente.</p>'
                        }
                    }
                ]
            )
            seccion_api.add_child(instance=articulo_api_auth)
            articulo_api_auth.save_revision().publish()

            # Configurar como página de inicio
            site.root_page = manual_home
            site.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Manual creado exitosamente!\n'
                    f'📱 Visita: http://localhost:8000/\n'
                    f'⚙️  Admin: http://localhost:8000/admin/\n'
                    f'📚 Se crearon {ManualHomePage.objects.count()} página principal, '
                    f'{SeccionPage.objects.count()} secciones, '
                    f'{SubseccionPage.objects.count()} subsecciones y '
                    f'{ArticuloPage.objects.count()} artículos'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al crear el manual: {str(e)}')
            )