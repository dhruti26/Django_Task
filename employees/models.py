from django.db import models

#Creating database models
class Employee(models.Model):
    """Model for storing employee details in sqlite database configure using settings.py."""
    name=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15)

    def __str__(self):
        return self.name

