# pages/models.py (or jobs/models.py depending on your app setup)
from django.db import models


class ContactMessage(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  subject = models.CharField(max_length=200)
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  is_resolved = models.BooleanField(default=False)

  class Meta:
    ordering = ["-created_at"]

  def __str__(self):
    return f"{self.subject} - {self.name} ({self.email})"