# Generated by Django 5.0 on 2023-12-12 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default=None, max_length=4, null=True, verbose_name='токен'),
        ),
    ]
