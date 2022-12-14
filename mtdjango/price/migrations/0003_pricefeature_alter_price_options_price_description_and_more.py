# Generated by Django 4.1.3 on 2022-11-25 09:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('price', '0002_rename_tiile_price_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='price',
            options={'ordering': ('price',)},
        ),
        migrations.AddField(
            model_name='price',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='userprice',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprice', to='price.price'),
        ),
        migrations.AlterField(
            model_name='userprice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprice', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PriceFeaturePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='price.price')),
                ('price_feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='price.pricefeature')),
            ],
            options={
                'ordering': ('price_id',),
            },
        ),
    ]
