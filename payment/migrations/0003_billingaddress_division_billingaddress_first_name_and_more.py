# Generated by Django 4.2.11 on 2024-05-07 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_billingaddress_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='division',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
