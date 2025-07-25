from django.db import models

class Application(models.Model):
    application_status = (
        ('submited', 'Submited'),
        ('rejected', 'Rejected'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
    )
    applicant = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    application_letter = models.TextField()
    status = models.CharField(max_length=50, choices=application_status)
    application_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['applicant', 'job']
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"