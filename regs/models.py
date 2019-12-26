from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

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

class Token(models.Model):
    ROLE = (('guest', 'Guest'), ('admin', 'Admin'))
    token = models.CharField(max_length = 100, blank = True, editable = False)
    role = models.CharField(max_length = 10, choices = ROLE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.user} ({self.get_role_display()})'

    def save(self, *args, **kwargs):
        self.token = get_random_string(32)
        super(Token, self).save(*args, **kwargs)

class News(models.Model):
    title = models.CharField(max_length = 200)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'News'
