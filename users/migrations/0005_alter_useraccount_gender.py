# Generated by Django 4.2.11 on 2024-05-06 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_vendoraccount_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]
