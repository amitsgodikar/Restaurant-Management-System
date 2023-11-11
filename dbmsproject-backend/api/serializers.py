from rest_framework import serializers
from .models import *



class OrderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderData
        fields = '__all__'


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class InventoryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        fields = '__all__'


class FoodItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItems
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class AllOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllOrders
        fields = '__all__'


class NewOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewOrder
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class ContainsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contains
        fields = '__all__'


class HasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Has
        fields = '__all__'


class StaffAbsentDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAbsentDays
        fields = '__all__'


class TakesFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakesFrom
        fields = '__all__'

class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffList
        fields = '__all__'

class StaffPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPayment
        fields = '__all__'

class BillSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillSummary
        fields = '__all__'

class ExpSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpSummary
        fields = '__all__'
