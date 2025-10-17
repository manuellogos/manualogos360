from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from wagtail.models import Site, Page

from manual.models import ManualHomePage

User = get_user_model()


class Command(BaseCommand):
    help = 'Inicializa el sitio con datos básicos para producción'

    def handle(self, *args, **options):
        # Crear superusuario si no existe
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@localhost', 'admin123')
            self.stdout.write(
                self.style.SUCCESS('✅ Superusuario "admin" creado con contraseña "admin123"')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Superusuario "admin" ya existe')
            )

        # Configurar homepage si no existe
        site = Site.objects.get(is_default_site=True)
        
        # Verificar si ya tenemos una ManualHomePage
        manual_pages = ManualHomePage.objects.all()
        
        if not manual_pages.exists():
            try:
                # Crear página de inicio del manual
                home_page = ManualHomePage(
                    title='Manual de Usuario - Logos360',
                    slug='home',
                    intro='Bienvenido al manual de usuario de Logos360. Encuentra toda la información que necesitas para usar nuestra plataforma.'
                )
                
                # Añadir como hijo de la página raíz
                root = site.root_page
                root.add_child(instance=home_page)
                home_page.save_revision().publish()
                
                # Configurar como página de inicio del sitio
                site.root_page = home_page
                site.hostname = 'manualogos360.onrender.com'
                site.site_name = 'Manual de Usuario - Logos360'
                site.save()
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Página de inicio del manual creada y configurada')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error creando página de inicio: {e}')
                )
        else:
            # Configurar sitio con página existente
            try:
                manual_page = manual_pages.first()
                site.root_page = manual_page
                site.hostname = 'manualogos360.onrender.com'
                site.site_name = 'Manual de Usuario - Logos360'
                site.save()
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Sitio configurado con página existente')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error configurando sitio: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Inicialización completada!')
        )
        self.stdout.write(
            self.style.SUCCESS('   Sitio disponible en: https://manualogos360.onrender.com/')
        )
        self.stdout.write(
            self.style.SUCCESS('   Admin disponible en: https://manualogos360.onrender.com/admin/')
        )
        self.stdout.write(
            self.style.SUCCESS('   Usuario: admin')
        )
        self.stdout.write(
            self.style.SUCCESS('   Contraseña: admin123')
        )