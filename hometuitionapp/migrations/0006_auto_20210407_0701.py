# Generated by Django 3.1.3 on 2021-04-07 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hometuitionapp', '0005_auto_20210406_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='monthly_fee',
        ),
        migrations.AlterField(
            model_name='teacher',
            name='education',
            field=models.CharField(choices=[('Secondary Level', 'Secondary Level'), ('Higher Secondary Level(Pursuing)', 'Higher Secondary Level(Pursuing)'), ('Higher Secondary Level(Completed)', 'Higher Secondary Level(Completed)'), ('Bachelors Degree(Pursuing)', 'Bachelors Degree(Pursuing)'), ('Bachelors Degree(Completed)', 'Bachelors Degree(Completed)'), ('Masters Degree(Pursuing)', 'Masters Degree(Pursuing)'), ('Masters Degree(Completed)', 'Masters Degree(Completed)')], max_length=100),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='training_license',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=30),
        ),
    ]