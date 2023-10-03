from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def clear_description(value):
    result = strip_tags(value)  # Удаляем HTML-теги
    # result = mark_safe(result)  # Помечаем строку как безопасную
    # result = result.replace('&mdash;', '')  # Удаляем символ &mdash;
    # result = result[:190]  # Отрезаем строку после 190 символов
    return result
