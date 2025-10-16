from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page


class ManualHomePage(Page):
    """Página principal del manual de usuario"""
    intro = RichTextField(
        blank=True,
        help_text="Introducción principal del manual"
    )
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Imagen principal del manual"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('hero_image'),
        FieldPanel('intro'),
    ]
    
    max_count = 1
    subpage_types = ['manual.SeccionPage']
    
    class Meta:
        verbose_name = "Página Principal del Manual"


class SeccionPage(Page):
    """Secciones principales del manual"""
    descripcion = RichTextField(
        blank=True,
        help_text="Descripción de la sección"
    )
    icono = models.CharField(
        max_length=50,
        blank=True,
        help_text="Clase CSS del icono (ej: fa-book, fa-settings)"
    )
    imagen_seccion = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Imagen representativa de la sección"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('icono'),
            FieldPanel('imagen_seccion'),
        ], heading="Configuración Visual"),
        FieldPanel('descripcion'),
    ]
    
    parent_page_types = ['manual.ManualHomePage']
    subpage_types = ['manual.SubseccionPage', 'manual.ArticuloPage']
    
    def get_articulos(self):
        """Obtiene todos los artículos de esta sección y subsecciones"""
        articulos = []
        for child in self.get_children().live():
            if hasattr(child.specific, 'contenido'):
                articulos.append(child.specific)
            elif hasattr(child.specific, 'get_articulos'):
                articulos.extend(child.specific.get_articulos())
        return articulos
    
    class Meta:
        verbose_name = "Sección"


class SubseccionPage(Page):
    """Subsecciones dentro de una sección"""
    descripcion = RichTextField(
        blank=True,
        help_text="Descripción de la subsección"
    )
    imagen_subseccion = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Imagen representativa de la subsección"
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('imagen_subseccion'),
        FieldPanel('descripcion'),
    ]
    
    parent_page_types = ['manual.SeccionPage']
    subpage_types = ['manual.ArticuloPage']
    
    def get_articulos(self):
        """Obtiene todos los artículos de esta subsección"""
        return [child.specific for child in self.get_children().live() 
                if hasattr(child.specific, 'contenido')]
    
    class Meta:
        verbose_name = "Subsección"


class ArticuloPage(Page):
    """Artículos individuales del manual"""
    imagen_destacada = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Imagen destacada del artículo"
    )
    contenido = StreamField([
        ('parrafo', blocks.RichTextBlock(
            label="Párrafo",
            help_text="Contenido de texto enriquecido"
        )),
        ('codigo', blocks.StructBlock([
            ('lenguaje', blocks.CharBlock(
                required=False,
                help_text="Lenguaje de programación (ej: python, javascript)"
            )),
            ('codigo', blocks.TextBlock(
                help_text="Código fuente"
            )),
        ], label="Bloque de código")),
        ('imagen', ImageChooserBlock(
            label="Imagen",
            help_text="Imagen ilustrativa"
        )),
        ('galeria', blocks.ListBlock(
            ImageChooserBlock(),
            label="Galería de imágenes",
            help_text="Múltiples imágenes en una galería"
        )),
        ('imagen_con_texto', blocks.StructBlock([
            ('imagen', ImageChooserBlock()),
            ('posicion', blocks.ChoiceBlock(choices=[
                ('left', 'Izquierda'),
                ('right', 'Derecha'),
                ('center', 'Centro'),
            ], default='left')),
            ('texto', blocks.RichTextBlock()),
        ], label="Imagen con texto", help_text="Imagen acompañada de texto")),
        ('alerta', blocks.StructBlock([
            ('tipo', blocks.ChoiceBlock(choices=[
                ('info', 'Información'),
                ('warning', 'Advertencia'),
                ('error', 'Error'),
                ('success', 'Éxito'),
            ])),
            ('titulo', blocks.CharBlock(required=False)),
            ('contenido', blocks.RichTextBlock()),
        ], label="Alerta")),
    ], blank=True, use_json_field=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('imagen_destacada'),
        FieldPanel('contenido'),
    ]
    
    parent_page_types = ['manual.SeccionPage', 'manual.SubseccionPage']
    
    def get_previous_article(self):
        """Obtiene el artículo anterior en la estructura"""
        siblings = self.get_parent().get_children().live().order_by('path')
        siblings_list = list(siblings)
        try:
            current_index = siblings_list.index(self)
            if current_index > 0:
                return siblings_list[current_index - 1].specific
        except ValueError:
            pass
        return None
    
    def get_next_article(self):
        """Obtiene el siguiente artículo en la estructura"""
        siblings = self.get_parent().get_children().live().order_by('path')
        siblings_list = list(siblings)
        try:
            current_index = siblings_list.index(self)
            if current_index < len(siblings_list) - 1:
                return siblings_list[current_index + 1].specific
        except ValueError:
            pass
        return None
    
    def get_section(self):
        """Obtiene la sección padre del artículo"""
        parent = self.get_parent().specific
        if isinstance(parent, SeccionPage):
            return parent
        elif isinstance(parent, SubseccionPage):
            return parent.get_parent().specific
        return None
    
    class Meta:
        verbose_name = "Artículo"
