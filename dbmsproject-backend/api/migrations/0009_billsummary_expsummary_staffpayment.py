# Generated by Django 3.2.3 on 2021-06-01 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_stafflist'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateField()),
            ],
            options={
                'db_table': 'staff_payment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BillSummary',
            fields=[
                ('month', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('expense', models.FloatField()),
                ('income', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ExpSummary',
            fields=[
                ('cat', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('sum', models.FloatField()),
            ],
        ),
    ]
