from django.db import models
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Для красивого отображения в админке
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="news",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='news',
        null=True,
        blank=True
    )
    # Для красивого отображения в админке
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def __str__(self):
        return self.title
