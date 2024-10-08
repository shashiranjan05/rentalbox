# Generated by Django 5.1 on 2024-08-29 13:37

import django.db.models.deletion
import django.utils.timezone
import phone_field.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('role', models.CharField(choices=[('CUSTOMER', 'CUSTOMER'), ('ADMIN', 'ADMIN')], default='CUSTOMER', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EnquiryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enquiry_id', models.CharField(max_length=64, null=True)),
                ('customer_name', models.CharField(max_length=64, null=True)),
                ('your_email', models.EmailField(max_length=128, null=True)),
                ('phone_number', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('org_details', models.CharField(max_length=64, null=True)),
                ('your_requirement', models.CharField(max_length=64, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalesQuoteDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=264, null=True)),
                ('product_id', models.CharField(max_length=128, null=True)),
                ('product_details', models.CharField(max_length=128, null=True)),
                ('time_period', models.CharField(choices=[('3 Months', '3 Months'), ('6 Months', '6 Months'), ('9 Months', '9 Months'), ('1 Year', '1 Year')], default='Other', max_length=200, null=True)),
                ('pricing', models.CharField(max_length=64, null=True)),
                ('enquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.enquirydetails')),
            ],
        ),
        migrations.CreateModel(
            name='CompleteDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('enquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.enquirydetails')),
                ('salesquote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.salesquotedetails')),
            ],
        ),
    ]
