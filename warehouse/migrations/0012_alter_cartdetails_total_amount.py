# Generated by Django 5.1 on 2024-09-07 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0011_alter_cartdetails_total_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartdetails',
            name='total_amount',
            field=models.IntegerField(null=True),
        ),
    ]
