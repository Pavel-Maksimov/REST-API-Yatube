# Generated by Django 3.2.3 on 2021-05-31 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210531_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(default=2, unique=True, verbose_name='Слаг'),
            preserve_default=False,
        ),
    ]
