from django import template

register = template.Library()

# Фильтр для добавления класса к полю формы
@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={'class': css})

# Тег для замены GET-параметров (пагинация, фильтры)
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    request = context['request']
    d = request.GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
