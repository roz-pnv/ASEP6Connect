from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()

class StudentState(models.TextChoices):
    GUIDED = 'Guided', 'Guided'
    WAITING = 'Waiting', 'Waiting'
    NOT_REGISTERED = 'NotRegistered', 'Not Registered'


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
    state = models.CharField(
        max_length=20, 
        choices=StudentState.choices,
        help_text="Guidance status of the student (Guided, Waiting, Not Registered)"
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
        help_text="Date the student arrived"
    )
    guidance_needed = models.BooleanField(
        default=False,
        help_text="Does the student need guidance?"
    )
    in_person_assistance = models.BooleanField(
        default=False,
        help_text="Has the student requested in-person assistance?"
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
			models.Index(fields=['state']),
			models.Index(fields=['guidance_needed']),
			models.Index(fields=['in_person_assistance']),
		]
        
    @property
    def stay_duration(self):
        """Calculate how many days the student has stayed since arrival."""
        if self.arrival_date:
            return (date.today() - self.arrival_date).days
        return 0
        
    def __str__(self):
    	return f"{self.user.username} - {self.field_of_study}"
    