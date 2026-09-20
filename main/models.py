import uuid

from django.db import models


class Experience(models.Model):
    CATEGORY_CHOICES = [
        ("INTERNSHIP", "Internship"),
        ("ORGANIZATION", "Organization"),
        ("COMPETITION", "Competition"),
        ("VOLUNTEERING", "Volunteering"),
        ("OTHER", "Other"),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    is_ongoing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)          
    description = models.TextField()                  
    year = models.TextField()                      

    def __str__(self):
        return self.title
