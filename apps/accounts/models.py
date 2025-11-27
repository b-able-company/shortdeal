from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """커스텀 유저 모델 - Creator/Buyer/Admin 역할 구분"""
    
    class Role(models.TextChoices):
        CREATOR = 'creator', '제작사'
        BUYER = 'buyer', '바이어'
        ADMIN = 'admin', '관리자'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CREATOR,
        verbose_name='역할'
    )
    company_name = models.CharField(max_length=100, blank=True, verbose_name='회사명')
    phone = models.CharField(max_length=20, blank=True, verbose_name='연락처')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
