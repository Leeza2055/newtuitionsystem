# Generated by Django 3.1.3 on 2021-04-09 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hometuitionapp', '0013_auto_20210409_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]