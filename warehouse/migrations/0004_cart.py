# Generated by Django 5.1 on 2024-08-31 11:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_cartdetails_total_amount_alter_cartdetails_qty_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('razor_pay_order_id', models.CharField(max_length=64, null=True)),
                ('razor_pay_payment_id', models.CharField(max_length=64, null=True)),
                ('razor_pay_payment_signature', models.CharField(max_length=64, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
