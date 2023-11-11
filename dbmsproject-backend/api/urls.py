from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview),
    path('bill/', views.show_bill),
    path('customer/', views.show_customer),
    path('inventoryitems/', views.show_inventory_items),
    path('fooditems/', views.ShowFoodItems),
    path('orders/', views.ShowOrders),
    path('staff/', views.ShowStaff),
    path('supplier/', views.ShowSupplier),
    path('contains/', views.ShowContains),
    path('has/', views.ShowHas),
    path('staffabsentdays/', views.ShowStaffAbsentDays),
    path('takesfrom/', views.ShowTakesFrom),
    path('payorder/', views.ToggleOrder),
    path('getStaff/', views.ShowAllStaff),
    path('payStaff/', views.PayStaff),
    path('bs/', views.G1Data),
    path('es/', views.G2Data),
    path('pd/', views.PDish),
    path('avg/', views.Avg),
    path('tcus/', views.Tcus),
    path('upit/', views.UpdateInventory),
    path('genbill/', views.generate_bill),
    path('fetchdata/', views.fetch_data),
    path('getpdf/', views.genpdf)
]
