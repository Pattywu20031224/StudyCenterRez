# Generated by Django 3.1.4 on 2021-06-20 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stu_rep',
            name='rep',
        ),
    ]
