# Generated by Django 3.1.3 on 2021-04-08 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hometuitionapp', '0008_remove_hiring_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='hiring',
            name='reject',
            field=models.BooleanField(default=False),
        ),
    ]
