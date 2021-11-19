import logging

from celery import shared_task
from django.core.mail import send_mail as django_send_mail

from bookstoreapi.apps.bookstores.models import StoreBookSubscription

logger = logging.getLogger("main")


@shared_task(name="process_subscription_notification")
def process_subscription_notification(store_book_id):
    subscribers = (
        StoreBookSubscription.objects.select_related(
            "store_book", "subscriber", "store_book__book"
        )
        .filter(store_book_id=store_book_id)
        .all()
    )
    if subscribers:
        send_email(
            f"{subscribers[0].store_book.book.name} book is now Available",
            message="Grab your now",
            sender="bookstore@support.com",
            to_list=[user.subscriber.email for user in subscribers],
            fail_silently=False,
        )


@shared_task(name="process_emails")
def send_email(subject, message, sender, to_list, fail_silently, **kwargs):
    logger.info(f"Sending mail to {str(to_list)}")
    result = django_send_mail(
        subject, message, sender, to_list, fail_silently=fail_silently, **kwargs
    )
    return "Email sent successful" if result == 1 else "Email was not sent"
