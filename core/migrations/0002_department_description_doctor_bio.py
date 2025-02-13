# Generated by Django 5.1.5 on 2025-02-10 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='description',
            field=models.TextField(default='No description available'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='bio',
            field=models.TextField(default='No descriptions available.'),
            preserve_default=False,
        ),
    ]
