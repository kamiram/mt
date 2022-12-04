from django.db import models


class EMail(models.Model):
    uid = models.CharField(max_length=100, unique=True, null=False)
    topic = models.CharField(max_length=200)
    mail_from = models.CharField(max_length=500)
    mail_to = models.CharField(max_length=500)
    sent = models.DateTimeField(max_length=200)
    read = models.DateTimeField(max_length=200, null=True)
    is_sent = models.BooleanField(default=False)
    readcount = models.IntegerField(null=True, default=-1)

    def __str__(self):
        return f'{self.mail_from} -> {self.mail_to}: {self.topic}'


class Constants(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} = {self.value}'
