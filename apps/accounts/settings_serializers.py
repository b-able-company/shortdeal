"""
Serializers for Settings/Profile management
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile (read and update)"""

    logo_url = serializers.SerializerMethodField()
    booth_slug = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'role',
            'company_name', 'logo_url', 'country',
            'genre_tags', 'booth_slug', 'is_onboarded'
        )
        read_only_fields = ('id', 'email', 'role', 'booth_slug', 'is_onboarded')

    def get_logo_url(self, obj):
        """Get logo URL if exists"""
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""

    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        """Validate current password is correct"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect")
        return value

    def validate(self, attrs):
        """Validate new passwords match"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': "New passwords do not match"
            })
        return attrs

    def save(self, **kwargs):
        """Update user password"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
