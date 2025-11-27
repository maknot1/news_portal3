from django import forms
from django.core.exceptions import ValidationError

from .models import News

class NewsForm(forms.ModelForm):

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if not title:
            raise ValidationError("Заголовок обязателен.")

        if len(title) < 5:
            raise ValidationError("Заголовок слишком короткий (минимум 5 символов).")

        return title

    def clean_text(self):
        text = self.cleaned_data.get('text')

        if not text:
            raise ValidationError("Текст обязателен.")

        if len(text) < 20:
            raise ValidationError("Текст слишком короткий (минимум 20 символов).")

        return text

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if title and text and title.strip() == text.strip():
            raise ValidationError("Текст новости не должен совпадать с заголовком.")

        return cleaned_data

    class Meta:
        model = News
        fields = '__all__'