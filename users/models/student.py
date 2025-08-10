from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()

class AccommodationType(models.TextChoices):
    DORMITORY = 'Dormitory', 'Dormitory'
    TEMPORARY = 'Temporary Housing', 'Temporary Housing'
    HOTEL = 'Hotel', 'Hotel'
    OTHER = 'Other', 'Other'


class Student(models.Model):
    user = models.ForeignKey(
        Users, 
        on_delete=models.CASCADE, 
        related_name='student_profiles',
        help_text="The user account associated with this student"
    )
    accommodation_type = models.CharField(
        max_length=50, 
        choices=AccommodationType.choices, 
        default=AccommodationType.DORMITORY,
        help_text="Type of accommodation (Dormitory, Temporary Housing, Hotel, Other)"
    )
    field_of_study = models.CharField(
        max_length=100,
        help_text="Student's academic field or major"
    )
    arrival_date = models.DateField(
        null=True, 
        blank=True,
        help_text="Date the student arrived"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date this student profile was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date when the student record was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
        indexes = [
			models.Index(fields=['arrival_date']),
		]
        
    @property
    def stay_duration(self):
        """Calculate how many days the student has stayed since arrival."""
        if self.arrival_date:
            return (date.today() - self.arrival_date).days
        return 0
        
    def __str__(self):
    	return f"{self.user.username} - {self.field_of_study}"
    