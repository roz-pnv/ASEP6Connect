from django.db import models  
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class GenderChoices(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'
    
class User(AbstractUser):
    first_name = models.CharField(
        max_length=30,
        help_text="User's first name"
    )
    last_name = models.CharField(
        max_length=30,
        help_text="User's last name"
    )
    gender = models.CharField(
		max_length=10,
		choices=GenderChoices.choices,
		blank=True,
		null=True,
		help_text="User's gender identity"
	)
    job = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="User's current job or occupation"
    )
    phone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^(?:\+33|0)[67]\d{8}$',
                message='Enter a valid French mobile number (e.g. +336xxxxxxxx or 06xxxxxxxx).'
            )
        ],
        blank=True,
        null=True,
        help_text="User's mobile phone number (French format)"
    )
    email = models.EmailField(
        unique=True,
        help_text="User's email address (must be unique)"
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="User's residential or mailing address"
    )
    language = models.CharField(
        max_length=10,
        default='fa',
        help_text="Preferred language for communication (e.g. fa, en, fr)"
    )
    birthdate = models.DateField(
        blank=True,
        null=True,
        help_text="User's date of birth"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is the user account currently active?"
    )
    is_boardofdirector = models.BooleanField(
        default=False,
        help_text="Is the user a member of the board of directors?"
    )
    is_student = models.BooleanField(
		default=False,
		help_text="Is the user a student?"
	)
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date the user account was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date when the user record was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['first_name']),
			models.Index(fields=['last_name']),
			models.Index(fields=['created_at']),
			models.Index(fields=['is_active']),
			models.Index(fields=['is_boardofdirector']),
        ]

    def __str__(self):
        return f"{self.username} ({self.email})"
