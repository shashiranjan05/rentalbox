# Generated by Django 5.1 on 2024-09-05 01:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0007_myorder_delete_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=264, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('name', models.CharField(max_length=264, null=True)),
                ('categories', models.CharField(choices=[('APPLIANCES', 'APPLIANCES'), ('ELECTRONICS', 'ELECTRONICS'), ('FURNITURE', 'FURNITURE')], default='Other', max_length=200, null=True)),
                ('description', models.CharField(max_length=1264, null=True)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=25)),
                ('is_available', models.BooleanField(default=True)),
                ('stock', models.PositiveIntegerField()),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='salesquotedetails',
            name='product_obj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.products'),
        ),
    ]
