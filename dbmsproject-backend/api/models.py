from django.db import models


class Data(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    timer = models.IntegerField()


class Bill(models.Model):
    bill_no = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    total_amount = models.FloatField()
    sup = models.ForeignKey('Supplier', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bill'


class Contains(models.Model):
    quantity = models.IntegerField()
    order = models.OneToOneField('Orders', models.DO_NOTHING)
    food = models.OneToOneField('FoodItems', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'contains'
        unique_together = (('order', 'food'),)

    def __str__(self):
        return self.order

class Customer(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, blank=True, null=True)
    customer_id = models.AutoField(db_column='customer_ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'

    def __str__(self):
        return self.customer_id

class FoodItems(models.Model):
    food_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'food_items'


class Has(models.Model):
    quantity = models.IntegerField()
    bill_no = models.OneToOneField(Bill, models.DO_NOTHING, db_column='bill_no')
    itemid = models.OneToOneField('InventoryItems', models.DO_NOTHING, db_column='itemID')  # Field name made lowercase.
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'has'
        unique_together = ('bill_no', 'itemid')


class InventoryItems(models.Model):
    itemid = models.AutoField(db_column='itemID', primary_key=True)  # Field name made lowercase.
    item_name = models.CharField(max_length=30)
    total_quantity = models.IntegerField()
    category = models.CharField(max_length=30, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory_items'

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    payment_status = models.CharField(max_length=10)
    date_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    payment_mode = models.CharField(max_length=10)
    amount = models.FloatField()
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='customer_ID')  # Field name made lowercase.
    staff = models.ForeignKey('Staff', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return str(self.order_id)

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    address = models.CharField(max_length=150)
    salary = models.FloatField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'staff'

    def __str__(self):
        return self.first_name

class StaffAbsentDays(models.Model):
    absent_days = models.DateField()
    staff = models.ForeignKey(Staff, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'staff_absent_days'
        unique_together = (('absent_days', 'staff'),)


class Supplier(models.Model):
    sup_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=30)
    address = models.CharField(max_length=150)
    email = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=15)
    website = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supplier'

    def __str__(self):
        return self.supplier_name

class TakesFrom(models.Model):
    quantity = models.IntegerField()
    staff = models.OneToOneField(Staff, models.DO_NOTHING, primary_key=True)
    itemid = models.ForeignKey(InventoryItems, models.DO_NOTHING, db_column='itemID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'takes_from'
        unique_together = (('staff', 'itemid'),)

class AllOrders(models.Model):
    order_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    amount = models.FloatField()
    payment_status = models.CharField(max_length=10)

class NewOrder(models.Model):
    order = models.JSONField()
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    amount = models.FloatField()
    payment_status = models.CharField(max_length=10)
    payment_mode = models.CharField(max_length=10)

class StaffList(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, blank=True, null=True)
    no_absent_days = models.IntegerField()
    salary = models.FloatField()

class StaffPayment(models.Model):
    amount = models.FloatField()
    date = models.DateField()
    staff = models.ForeignKey(Staff, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'staff_payment'
        unique_together = (('date', 'staff'),)

class BillSummary(models.Model):
    month = models.CharField(max_length=15, primary_key=True)
    expense = models.FloatField()
    income = models.FloatField()

class ExpSummary(models.Model):
    cat = models.CharField(primary_key=True, max_length=100)
    sum = models.FloatField()

class OrderData(models.Model):
    month = models.CharField(primary_key=True, max_length=15)
    sales = models.IntegerField()

class PdfBill(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    quantity = models.IntegerField
    price = models.FloatField
    amount = models.FloatField()
