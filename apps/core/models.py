from django.db import models


class Account(models.Model):
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=75)

    def __str__(self):
        return self.email


class Friend(models.Model):
    name = models.CharField(max_length=200)
    profile_url = models.URLField(default='https://mbasic.facebook.com')
    current_city = models.CharField(max_length=250, blank=True, null=True)
    hometown = models.CharField(max_length=250, blank=True, null=True)
    friend_of = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='friends')

    def __str__(self):
        return self.name
