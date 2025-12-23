from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from newsportal.models import Post, Category
from newsportal3 import settings


@shared_task
def notify_subscribers():
    post = Post.objects.get(id=post_id)
    subscribers = post.category.subscribers.all()

    emails = [user.email for user in subscribers if user.email]

    if emails:
        send_mail(
            subject=f"Новая новость {post.title}",
            message=post.content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
        )


@shared_task
def weekly_newsletter():
    last_week = now() - timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)

    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        emails = [u.email for u in subscribers if u.email]

        category_posts = posts.filter(category=category)
        if not emails or not category_posts:
            continue

        text = "\n\n".join(p.content for p in category_posts)

        send_mail(
            subject="Еженедельная подборка новостей",
            message=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
        )