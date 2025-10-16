from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from wagtail.models import Site

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
        
        if not hasattr(site.root_page, 'manualhomepage'):
            # Crear página de inicio del manual
            home_page = ManualHomePage(
                title='Manual de Usuario',
                slug='manual',
                intro='Bienvenido al manual de usuario. Encuentra toda la información que necesitas.'
            )
            
            # Añadir como hijo de la página raíz
            site.root_page.add_child(instance=home_page)
            
            # Configurar como página de inicio del sitio
            site.root_page = home_page
            site.save()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Página de inicio del manual creada y configurada')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  La página de inicio del manual ya existe')
            )

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Inicialización completada!')
        )
        self.stdout.write(
            self.style.SUCCESS('   Puedes acceder al admin en /admin/')
        )
        self.stdout.write(
            self.style.SUCCESS('   Usuario: admin')
        )
        self.stdout.write(
            self.style.SUCCESS('   Contraseña: admin123')
        )