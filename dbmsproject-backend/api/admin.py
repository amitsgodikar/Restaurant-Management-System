from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Bill)
admin.site.register(Contains)
admin.site.register(Customer)
admin.site.register(FoodItems)
admin.site.register(Has)
admin.site.register(InventoryItems)
admin.site.register(Orders)
admin.site.register(Staff)
admin.site.register(StaffAbsentDays)
admin.site.register(Supplier)
admin.site.register(TakesFrom)

