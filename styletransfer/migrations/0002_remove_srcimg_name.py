# Generated by Django 3.1.2 on 2021-06-29 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('styletransfer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='srcimg',
            name='name',
        ),
    ]