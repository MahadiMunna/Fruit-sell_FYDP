# Generated by Django 3.2.25 on 2024-06-21 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0016_comment_image_comment_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='fruitmodel',
            name='blockchain_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]