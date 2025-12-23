from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import News, Post

User = get_user_model()


@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        notify_subscribers.delay(instance.id)

@receiver(pre_save, sender=News)
def news_pre_save(sender, instance, *args, **kwargs):
    if instance.pk:
        return

    today = now().date()

    news_count = News.objects.filter(
        author=instance.author,
        created_at__date=today
    ).count()

    if news_count >= 3:
        raise ValidationError(
            "Вы не можете публиковать более 3 новостей в сутки."
        )


@receiver(post_save, sender=User)
def create_user_to_common(sender, instance, created, **kwargs):
    if created:
        try:
            group = Group.objects.get(name='common')
            instance.groups.add(group)
        except Group.DoesNotExist:
            pass


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if not created:
        return


    User.objects.filter(pk=instance.pk).update(is_active=False)

    token = default_token_generator.make_token(instance)
    uid = urlsafe_base64_encode(force_bytes(instance.pk))

    activation_link = f"{settings.SITE_URL}/activate/{uid}/{token}/"

    # plain-text (стабильно для email)
    text_content = (
        f"Здравствуй, {instance.username}!\n\n"
        f"Добро пожаловать на сайт.\n\n"
        f"Для активации аккаунта перейдите по ссылке:\n"
        f"{activation_link}"
    )

    msg = EmailMessage(
        subject="Добро пожаловать!",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[instance.email],
    )
    msg.send()


@receiver(post_save, sender=News)
def notify_subscribers(sender, instance, created, **kwargs):
    if not created or not instance.category:
        return

    article_url = f"{settings.SITE_URL}{instance.get_absolute_url()}"
    subscribers = instance.category.subscribers.all()

    for user in subscribers:
        if not user.email:
            continue

        text_content = (
            f"Здравствуй, {user.username}!\n\n"
            f"В твоём любимом разделе вышла новая статья.\n\n"
            f"{instance.text[:150]}...\n\n"
            f"Читать полностью:\n{article_url}"
        )

        EmailMessage(
            subject=instance.title,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        ).send()
