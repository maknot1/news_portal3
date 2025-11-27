from django import template

register = template.Library()

BAD_WORDS = ['редиска', 'дурак', 'паразит']

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError('Фильтр censor применяется только к строкам')

    words = value.split()

    censored_text = []
    for word in words:
        base = word.lower()
        for bad in BAD_WORDS:
            if base.startswith(bad[0]) and base.startswith(bad):
                word = word[0] + '*' * (len(word) - 1)
        censored_text.append(word)

    return ' '.join(censored_text)