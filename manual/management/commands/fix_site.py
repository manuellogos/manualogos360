from django.core.management.base import BaseCommand
from wagtail.models import Site

from manual.models import ManualHomePage


class Command(BaseCommand):
    help = 'Arregla la configuración del sitio para que muestre el manual'

    def handle(self, *args, **options):
        try:
            # Obtener el sitio por defecto
            site = Site.objects.get(is_default_site=True)
            
            # Buscar una página del manual
            manual_page = ManualHomePage.objects.first()
            
            if manual_page:
                # Configurar el sitio para usar la página del manual
                site.root_page = manual_page
                site.hostname = 'manualogos360.onrender.com'
                site.site_name = 'Manual de Usuario - Logos360'
                site.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Sitio configurado correctamente')
                )
                self.stdout.write(
                    self.style.SUCCESS(f'   Página raíz: {manual_page.title}')
                )
                self.stdout.write(
                    self.style.SUCCESS(f'   Hostname: {site.hostname}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ No se encontró ninguna página ManualHomePage')
                )
                self.stdout.write(
                    self.style.WARNING('   Ejecuta: python manage.py setup_site'))
                
        except Site.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ No se encontró un sitio por defecto')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {e}')
            )