# Generated by Django 4.2.11 on 2024-05-07 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0002_vendor_fruitmodel_discount_fruitmodel_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fruitmodel',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=3, null=True),
        ),
    ]
