"""
Constants for ShortDeal application
"""

# Content status
CONTENT_STATUS_DRAFT = 'draft'
CONTENT_STATUS_PUBLIC = 'public'
CONTENT_STATUS_DELETED = 'deleted'

CONTENT_STATUS_CHOICES = [
    (CONTENT_STATUS_DRAFT, 'Draft'),
    (CONTENT_STATUS_PUBLIC, 'Public'),
    (CONTENT_STATUS_DELETED, 'Deleted'),
]

# Offer status
OFFER_STATUS_PENDING = 'pending'
OFFER_STATUS_ACCEPTED = 'accepted'
OFFER_STATUS_REJECTED = 'rejected'
OFFER_STATUS_EXPIRED = 'expired'

OFFER_STATUS_CHOICES = [
    (OFFER_STATUS_PENDING, 'Pending'),
    (OFFER_STATUS_ACCEPTED, 'Accepted'),
    (OFFER_STATUS_REJECTED, 'Rejected'),
    (OFFER_STATUS_EXPIRED, 'Expired'),
]

# Currency
CURRENCY_USD = 'USD'
CURRENCY_KRW = 'KRW'
CURRENCY_EUR = 'EUR'
CURRENCY_JPY = 'JPY'

CURRENCY_CHOICES = [
    (CURRENCY_USD, 'US Dollar'),
    (CURRENCY_KRW, 'Korean Won'),
    (CURRENCY_EUR, 'Euro'),
    (CURRENCY_JPY, 'Japanese Yen'),
]

# File upload limits
MAX_LOGO_SIZE = 2 * 1024 * 1024  # 2MB
MAX_THUMBNAIL_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg']
