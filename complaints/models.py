from django.db import models
from django.conf import settings
from django.utils import timezone

class Complaint(models.Model):
    """
    Model for storing student complaints
    """
    CATEGORY_CHOICES = (
        ('ragging', 'Ragging'),
        ('harassment', 'Harassment'),
        ('faculty', 'Faculty Misbehavior'),
        ('student', 'Student Misbehavior'),
        ('infrastructure', 'Infrastructure'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
        ('dismissed', 'Dismissed'),
    )
    
    # Auto-generated complaint ID
    complaint_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Who filed the complaint
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    
    # Complaint details
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    evidence = models.FileField(upload_to='evidence/', blank=True, null=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Admin archive/delete flags
    archived_by_admin = models.BooleanField(default=False)
    deleted_by_admin = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Auto-generate complaint ID like GRV-2025-001
        if not self.complaint_id:
            year = timezone.now().year
            
            # Get the highest complaint number for this year
            last_complaint = Complaint.objects.filter(
                complaint_id__startswith=f"GRV-{year}-"
            ).order_by('-complaint_id').first()
            
            if last_complaint:
                # Extract the number and increment
                try:
                    last_number = int(last_complaint.complaint_id.split('-')[-1])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            
            # Create complaint ID
            self.complaint_id = f"GRV-{year}-{new_number:03d}"
            
            # Double-check it doesn't exist (safety measure)
            while Complaint.objects.filter(complaint_id=self.complaint_id).exists():
                new_number += 1
                self.complaint_id = f"GRV-{year}-{new_number:03d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.complaint_id} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'


class Response(models.Model):
    """
    Admin responses to complaints
    """
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    responded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.complaint.complaint_id}"
    
    class Meta:
        ordering = ['responded_at']