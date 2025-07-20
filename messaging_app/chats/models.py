import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)

    # Explicit password_hash field (custom, stores hashed password)
    password_hash = models.CharField(max_length=128, null=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELD = 'username'  # or 'email' if you want email login

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        """
        If password_hash is set with plain text, hash it before saving.
        """
        from django.contrib.auth.hashers import make_password
        if not self.password_hash.startswith('pbkdf2_'):
            self.password_hash = make_password(self.password_hash)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """
        Check if the raw password matches the hashed password.
        """
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return f"{self.username} ({self.email})"
