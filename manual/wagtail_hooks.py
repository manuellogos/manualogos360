from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin import widgets


@hooks.register('construct_main_menu')
def hide_unwanted_menu_items(request, menu_items):
    """Ocultar elementos del menú que no necesitamos para el manual"""
    items_to_hide = ['snippets', 'forms', 'redirects']
    menu_items[:] = [item for item in menu_items if item.name not in items_to_hide]


@hooks.register('construct_settings_menu')
def hide_settings_menu_items(request, menu_items):
    """Personalizar el menú de configuración"""
    # Mantener solo los elementos esenciales
    essential_items = ['sites', 'users', 'groups', 'locales']
    menu_items[:] = [item for item in menu_items if getattr(item, 'name', '') in essential_items]


@hooks.register('insert_global_admin_css')
def global_admin_css():
    """CSS personalizado para el admin de Wagtail"""
    return format_html(
        '<style>'
        '.halloeditor {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }}'
        '.object-help {{ background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 10px; margin-bottom: 15px; }}'
        '.manual-section {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}'
        '</style>'
    )


@hooks.register('insert_global_admin_js')
def global_admin_js():
    """JavaScript personalizado para el admin"""
    return format_html(
        '<script>'
        'document.addEventListener("DOMContentLoaded", function() {{'
        '    console.log("Manual CMS Admin loaded");'
        '    var titleFields = document.querySelectorAll("input[name*=title]");'
        '    titleFields.forEach(function(field) {{'
        '        field.addEventListener("blur", function() {{'
        '            if (this.value && !document.querySelector("input[name*=slug]").value) {{'
        '                console.log("Auto-generating slug...");'
        '            }}'
        '        }});'
        '    }});'
        '}});'
        '</script>'
    )