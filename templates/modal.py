# Importing necessary libraries and modules
from django import template
from django.template.loader import get_template
from django.template import Context
from django.utils.safestring import mark_safe

# Creating a register object of the template Library class
register = template.Library()

@register.simple_tag
# Defining a function 'modal' utilizing the decorator '@register.simple_tag' 
# The purpose of this function is to render a modal with given parameters - modal_id, modal_title, modal_body, modal_footer
# modal_id: the ID of the modal
# modal_title: the title of the modal 
# modal_body: the body of the modal 
# modal_footer: the footer of the modal
# The function uses Django's Context and Template objects to render a HTML template for the modal, 
# which allows for template inheritance and reuse. The function then returns a safe string with the rendered HTML for the modal.
def modal(modal_id, modal_title='', modal_body='', modal_footer=''):
    context = Context({
        'modal_id': modal_id,  # The ID of the Modal
        'modal_title': modal_title, # The title of the Modal
        'modal_body': modal_body,  # The body of the Modal
        'modal_footer': modal_footer  # The footer of the Modal
    })
    # Get a Template object with the modal's HTML
    template = get_template('modal/modal.html')
    # Render the template with the context and return a safe string
    return mark_safe(template.render(context))