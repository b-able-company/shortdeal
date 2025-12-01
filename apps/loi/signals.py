"""
Signal handlers for LOI auto-generation
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.offers.models import Offer
from .models import LOI


@receiver(post_save, sender=Offer)
def create_loi_on_offer_accept(sender, instance, **kwargs):
    """
    Auto-create LOI when offer is accepted.
    Business Rule: Offer accept → LOI auto-create
    """
    # Only create LOI if offer was just accepted and LOI doesn't exist
    if instance.status == 'accepted' and not hasattr(instance, 'loi'):
        try:
            LOI.create_from_offer(instance)
        except Exception:
            # LOI already exists or creation failed
            pass
