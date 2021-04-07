# Generated by Django 3.1.3 on 2021-04-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hometuitionapp', '0002_subjectfee_teacherstudentfee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Disabled', 'Disabled')], default='Inactive', max_length=50, null=True)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='slider')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='teacherstudentfee',
            name='payment_status',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
