# Generated by Django 2.2.1 on 2019-05-14 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('machinestate', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='state_history',
            new_name='history',
        ),
    ]
