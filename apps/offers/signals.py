"""
Signal handlers for Offer notifications
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Offer


@receiver(post_save, sender=Offer)
def send_new_offer_notification(sender, instance, created, **kwargs):
    """
    Send email notification when new offer is created (NTF-001)
    """
    if created:
        from apps.notifications.emails import send_new_offer_notification as send_email
        try:
            send_email(instance)
        except Exception:
            pass  # Don't fail offer creation if email fails
