# Generated by Django 4.2.4 on 2023-12-15 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_alter_publication_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='publication_type',
            field=models.CharField(choices=[('for_all', 'доступна всем пользователям'), ('for_reg', 'доступна зарегистрированным пользователям'), ('for_sub', 'доступна пользователям с оплаченной подпиской')], default='for_all', max_length=7, verbose_name='тип публикации'),
        ),
        migrations.AddField(
            model_name='publication',
            name='views',
            field=models.IntegerField(default=0, verbose_name='просмотры'),
        ),
    ]