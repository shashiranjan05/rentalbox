# Generated by Django 5.1 on 2024-09-01 02:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0006_alter_cart_razor_pay_order_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('razor_pay_order_id', models.CharField(blank=True, max_length=64, null=True)),
                ('razor_pay_payment_id', models.CharField(blank=True, max_length=64, null=True)),
                ('razor_pay_payment_signature', models.CharField(blank=True, max_length=64, null=True)),
                ('cart', models.ManyToManyField(related_name='my_order', to='warehouse.cartdetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
