"""
Signal handlers for Booth auto-creation
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.core.utils import generate_unique_slug


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_booth_for_producer(sender, instance, created, **kwargs):
    """
    Auto-create booth when a producer (creator) user is created.
    Business Rule: Producer signup → Booth auto-creation
    """
    if created and instance.role == 'creator':
        from apps.booths.models import Booth

        # Generate unique slug from company name or username
        base_slug = instance.company_name or instance.username
        unique_slug = generate_unique_slug(Booth, base_slug, slug_field='slug')

        # Create booth
        booth = Booth.objects.create(
            producer=instance,
            slug=unique_slug
        )

        # Update user's booth_slug field
        instance.booth_slug = unique_slug
        instance.save(update_fields=['booth_slug'])
