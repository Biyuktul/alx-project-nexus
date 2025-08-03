from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, help_text="Brief description of the category")

    def __str__(self):
        return self.name

class Job(models.Model):
    types = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contractual', 'Contractual'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, db_index=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(max_length=20, choices=types)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='jobs', db_index=True)
    recruiter = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
          indexes = [
              models.Index(fields=['category', 'location'], name='job_category_location_idx'),
          ]