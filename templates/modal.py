from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def modal(modal_id, modal_title='', modal_body='', modal_footer=''):
    """Renders a modal with the given parameters.

    modal_id: the ID of the modal
    modal_title: the title of the modal
    modal_body: the body of the modal
    modal_footer: the footer of the modal

    Returns a safe string with the rendered HTML for the modal.
    """
    context = {
        'modal_id': modal_id,
        'modal_title': modal_title,
        'modal_body': modal_body,
        'modal_footer': modal_footer
    }
    return mark_safe(render_to_string('modal/modal.html', context))