# Generated by Django 3.2.3 on 2021-05-31 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210601_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stafflist',
            name='salary',
            field=models.FloatField(),
        ),
    ]
