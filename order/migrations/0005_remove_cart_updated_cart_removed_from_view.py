# Generated by Django 4.2.11 on 2024-05-13 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_order_delivery_status_order_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='updated',
        ),
        migrations.AddField(
            model_name='cart',
            name='removed_from_view',
            field=models.BooleanField(default=False),
        ),
    ]