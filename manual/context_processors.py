from wagtail.models import Site

from .models import ManualHomePage


def manual_navigation(request):
    """Context processor para la navegación del manual"""
    try:
        site = Site.find_for_request(request)
        if site:
            # Buscar la página principal del manual directamente
            manual_home = ManualHomePage.objects.filter(live=True).first()
            
            if manual_home:
                # Obtener todas las secciones (hijas directas de ManualHomePage)
                sections = manual_home.get_children().live().order_by('path')
                
                return {
                    'manual_home': manual_home,
                    'manual_sections': sections,
                }
    except Exception as e:
        # Log el error si es necesario para debugging
        print(f"Error in manual_navigation: {e}")
    
    return {
        'manual_home': None,
        'manual_sections': [],
    }