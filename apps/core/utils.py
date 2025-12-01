"""
Utility functions and helpers for ShortDeal
"""
from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet for soft delete functionality"""

    def delete(self):
        """Soft delete by setting status to 'deleted'"""
        return self.update(status='deleted', deleted_at=timezone.now())

    def hard_delete(self):
        """Actual database deletion"""
        return super().delete()

    def active(self):
        """Filter to exclude deleted items"""
        return self.exclude(status='deleted')


class SoftDeleteManager(models.Manager):
    """Manager for soft delete functionality"""

    def get_queryset(self):
        """Override to use SoftDeleteQuerySet"""
        return SoftDeleteQuerySet(self.model, using=self._db)

    def active(self):
        """Get only active (non-deleted) objects"""
        return self.get_queryset().active()


def generate_unique_slug(model_class, base_slug, slug_field='slug'):
    """
    Generate a unique slug by appending a counter if necessary

    Args:
        model_class: Django model class
        base_slug: Base slug string
        slug_field: Field name for slug (default: 'slug')

    Returns:
        Unique slug string
    """
    from django.utils.text import slugify

    slug = slugify(base_slug)
    unique_slug = slug
    counter = 1

    while model_class.objects.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1

    return unique_slug
