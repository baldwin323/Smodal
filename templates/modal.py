from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def modal(modal_id, modal_title='', modal_body='', modal_footer=''):
    context = {
        'modal_id': modal_id,
        'modal_title': modal_title,
        'modal_body': modal_body,
        'modal_footer': modal_footer
    }
    return mark_safe(render_to_string('modal.html', context))