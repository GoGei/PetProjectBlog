from django import template

register = template.Library()


@register.simple_tag
def get_message_class(message_tag):
    message_tag_map = {
        'debug': 'alert-light',
        'info': 'alert-info',
        'success': 'alert-success',
        'warning': 'alert-warning',
        'error': 'alert-danger',
        'default': 'alert-dark',
    }
    return message_tag_map.get(message_tag, 'default')
