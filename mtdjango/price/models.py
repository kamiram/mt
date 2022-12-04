from django.contrib.auth import get_user_model
from django.db import models


class Price(models.Model):
    title = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.title} / {self.price}'

    class Meta:
        ordering = ('price', )


class UserPrice(models.Model):
    price = models.ForeignKey(Price, null=False, on_delete=models.CASCADE, related_name='userprice')
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE, related_name='userprice')
    expire = models.DateTimeField(null=False)

    def __str__(self):
        return f'{self.user.username} / {self.price.title} / {self.expire}'


class PriceFeature(models.Model):
    code = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ('title', )


class PriceFeaturePrice(models.Model):
    price = models.ForeignKey(Price, null=False, on_delete=models.CASCADE)
    price_feature = models.ForeignKey(PriceFeature, null=False, on_delete=models.CASCADE)

    class Meta:
        ordering = ('price_id', )
