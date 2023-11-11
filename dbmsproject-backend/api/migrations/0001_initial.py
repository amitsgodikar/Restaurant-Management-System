# Generated by Django 3.2.3 on 2021-05-13 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('bill_no', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('total_amount', models.FloatField()),
            ],
            options={
                'db_table': 'bill',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('customer_id', models.AutoField(db_column='customer_ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'customer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FoodItems',
            fields=[
                ('food_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.FloatField()),
            ],
            options={
                'db_table': 'food_items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryItems',
            fields=[
                ('itemid', models.AutoField(db_column='itemID', primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=30)),
                ('total_quantity', models.IntegerField()),
                ('category', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'inventory_items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_status', models.CharField(max_length=10)),
                ('date_time', models.DateTimeField(blank=True, null=True)),
                ('payment_mode', models.CharField(max_length=10)),
                ('amount', models.FloatField()),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=150)),
                ('salary', models.FloatField()),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('designation', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'staff',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StaffAbsentDays',
            fields=[
                ('absent_days', models.DateField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'staff_absent_days',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('sup_id', models.AutoField(primary_key=True, serialize=False)),
                ('supplier_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=150)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile', models.IntegerField()),
                ('website', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'supplier',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contains',
            fields=[
                ('quantity', models.IntegerField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.orders')),
            ],
            options={
                'db_table': 'contains',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Has',
            fields=[
                ('quantity', models.IntegerField()),
                ('bill_no', models.OneToOneField(db_column='bill_no', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.bill')),
            ],
            options={
                'db_table': 'has',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TakesFrom',
            fields=[
                ('quantity', models.IntegerField()),
                ('staff', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.staff')),
            ],
            options={
                'db_table': 'takes_from',
                'managed': False,
            },
        ),
    ]
