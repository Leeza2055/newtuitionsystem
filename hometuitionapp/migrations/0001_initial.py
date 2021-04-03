# Generated by Django 3.1.4 on 2021-04-02 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Disabled', 'Disabled')], default='Inactive', max_length=50, null=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomeTuitionSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Disabled', 'Disabled')], default='Inactive', max_length=50, null=True)),
                ('name', models.CharField(max_length=40)),
                ('logo', models.ImageField(upload_to='logo')),
                ('about', models.TextField()),
                ('about_image1', models.ImageField(upload_to='system')),
                ('about_image2', models.ImageField(upload_to='system')),
                ('email', models.EmailField(max_length=254)),
                ('phone_no', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Disabled', 'Disabled')], default='Inactive', max_length=50, null=True)),
                ('name', models.CharField(max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hometuitionapp.course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Disabled', 'Disabled')], default='Inactive', max_length=50, null=True)),
                ('name', models.CharField(max_length=30)),
                ('gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE'), ('other', 'OTHER')], max_length=10)),
                ('photo', models.ImageField(upload_to='teacher')),
                ('phone_no', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=40)),
                ('education', models.CharField(max_length=100)),
                ('cv', models.FileField(upload_to='cv')),
                ('citizenship', models.FileField(upload_to='citizenship')),
                ('can_teach_location', models.TextField()),
                ('teaching_experience', models.TextField()),
                ('monthly_fee', models.PositiveIntegerField()),
                ('training_license', models.BooleanField()),
                ('availabilty', models.TextField()),
                ('reference_person', models.CharField(max_length=30)),
                ('reference_person_contact_no', models.CharField(max_length=30)),
                ('course', models.ManyToManyField(to='hometuitionapp.Course')),
                ('subject', models.ManyToManyField(to='hometuitionapp.Subject')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Disabled', 'Disabled')], default='Inactive', max_length=50, null=True)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=40)),
                ('phone_no', models.CharField(max_length=40)),
                ('tuition_type', models.CharField(choices=[('Single', 'Single'), ('Group', 'Group')], max_length=30)),
                ('salary', models.PositiveIntegerField()),
                ('time', models.CharField(max_length=70)),
                ('report_card', models.FileField(upload_to='report_card')),
                ('course', models.ManyToManyField(to='hometuitionapp.Course')),
                ('subject', models.ManyToManyField(to='hometuitionapp.Subject')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hometuitionapp.teacher')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hiring',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hire_date', models.DateTimeField(auto_now=True)),
                ('accept', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hometuitionapp.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hometuitionapp.teacher')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]