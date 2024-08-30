# Generated by Django 5.1 on 2024-08-30 11:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesquotedetails',
            name='added_to_cart',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salesquotedetails',
            name='qty',
            field=models.IntegerField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='salesquotedetails',
            name='sales_quote_id',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='salesquotedetails',
            name='sq_reject',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CartDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_period', models.CharField(choices=[('3 Months', '3 Months'), ('6 Months', '6 Months'), ('9 Months', '9 Months'), ('1 Year', '1 Year')], default='Other', max_length=200, null=True)),
                ('pricing', models.CharField(max_length=64, null=True)),
                ('qty', models.IntegerField(max_length=30, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('enquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.enquirydetails')),
                ('sq_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.salesquotedetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
