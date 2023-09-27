# Importing necessary libraries and modules
from django import template
from django.template.loader import get_template
from django.template import Context
from django.utils.safestring import mark_safe

# Creating a register object of the template Library class
register = template.Library()

@register.inclusion_tag('modal/modal.html')
# Defining a function 'modal' utilizing the decorator '@register.inclusion_tag' 
# The purpose of this function is to render a modal with given parameters - modal_id, modal_title, modal_body, modal_footer
# modal_id: the ID of the modal
# modal_title: the title of the modal 
# modal_body: the body of the modal 
# modal_footer: the footer of the modal
# This function returns a dictionary that tells Django how to render the modal template.
def modal(modal_id, modal_title='', modal_body='', modal_footer=''):
    return {
        'modal_id': modal_id,  # The ID of the Modal
        'modal_title': modal_title, # The title of the Modal
        'modal_body': modal_body,  # The body of the Modal
        'modal_footer': modal_footer,  # The footer of the Modal
    }