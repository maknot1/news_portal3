from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage

from .models import News, Category


def send_weekly_news_digest():
    print("🚀 send_weekly_news_digest TRIGGERED")

    now = timezone.now()
    week_ago = now - timedelta(days=7)

    for category in Category.objects.all():
        print(f"📂 Category: {category.name}")

        news_list = News.objects.filter(
            category=category,
            created_at__gte=week_ago
        )

        print(f"📰 Found news: {news_list.count()}")
        print(f"👤 Subscribers: {category.subscribers.count()}")

        if not news_list.exists():
            print("⛔ No news for this category, skipping")
            continue

        for user in category.subscribers.all():
            if not user.email:
                print(f"⚠️ User {user.username} has no email, skipping")
                continue

            print(f"✉️ Sending email to: {user.email}")

            lines = [
                f"Здравствуй, {user.username}!",
                "",
                f"Новые статьи в категории «{category.name}» за неделю:",
                ""
            ]

            for news in news_list:
                url = f"{settings.SITE_URL}{news.get_absolute_url()}"
                lines.append(f"- {news.title}")
                lines.append(f"  {url}")

            text_content = "\n".join(lines)

            EmailMessage(
                subject=f"Новые статьи за неделю - {category.name}",
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            ).send()

    print("✅ send_weekly_news_digest FINISHED")
