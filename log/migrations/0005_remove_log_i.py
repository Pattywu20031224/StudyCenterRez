# Generated by Django 3.1.4 on 2021-06-20 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0004_log_i'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='i',
        ),
    ]