# Generated by Django 2.2.1 on 2019-05-17 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machinestate', '0002_auto_20190514_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='machine_status',
            field=models.CharField(max_length=20),
        ),
    ]