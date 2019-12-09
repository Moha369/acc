from django.db import models
from django.contrib.auth.models import User

class Registration(models.Model):
    STATUSES = (('pending', 'Pending'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected'))
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    email = models.EmailField(unique = True, null = True)
    status = models.CharField(max_length = 100, choices = STATUSES, default = 'pending')
    message = models.TextField()

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length = 100)
    message = models.TextField(max_length = 500)
    STATUSES = (('pending', 'Pending'),
                ('replied', 'Replied'),
                ('ignored', 'Ignored'))
    status = models.CharField(max_length = 100, choices = STATUSES, default = 'pending')

    def __str__(self):
        return self.user.username
