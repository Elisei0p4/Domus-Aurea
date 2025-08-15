from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Позволяет получать значение из словаря по ключу-переменной в шаблоне Django.
    Использование: {{ my_dictionary|get_item:my_key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None