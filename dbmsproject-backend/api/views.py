import datetime
import io

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from django.db import connection
from reportlab.pdfgen import canvas
from django.http import FileResponse, HttpResponse
from django.template import loader
from io import BytesIO

from xhtml2pdf import pisa


@api_view(['POST'])
def genpdf(request):
    print(request.data)
    orderitem = PdfBill.objects.raw("SELECT name, quantity, price, price * quantity AS amount FROM contains, orders, food_items WHERE orders.order_id = contains.order_id AND contains.food_id = food_items.food_id AND orders.order_id = '%s';", [request.data])
    order = Orders.objects.get(order_id=request.data)
    customer = Customer.objects.get(customer_id=order.customer_id)
    total = sum(x.amount for x in orderitem)
    template = loader.get_template('index.html')
    context = {
        'results': orderitem,
        'order': order,
        'total': total,
        'customer': customer
    }
    temp = template.render(context, request)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(temp.encode("ISO-8859-1")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}".pdf'.format(order.order_id)
        return response
    return None


@api_view(['POST'])
def fetch_data(request):
    print(request.data)
    start = request.data['range']['start'][:10] + ' ' + request.data['range']['start'][11:19]
    end = request.data['range']['end'][:10] + ' ' + request.data['range']['end'][11:19]
    if request.data['data'] == 'Food Sales Data':
        data = Data.objects.raw("SELECT name, SUM(quantity) AS timer FROM contains, orders, food_items WHERE contains.food_id = food_items.food_id AND orders.order_id = contains.order_id AND date_time BETWEEN %s AND %s GROUP BY contains.food_id;", [start, end])
        serializer = DataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.data['data'] == 'Customer Data':
        data = OrderData.objects.raw("SELECT MONTHNAME(date_time) AS month, COUNT(*) AS sales FROM orders GROUP BY MONTH(date_time);")
        serializer = OrderDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def generate_bill(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.line(100,100,20,20)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='test.pdf')


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Staff': '/staff'
    }
    return Response(api_urls)


@api_view(['GET', 'POST'])
def show_bill(request):
    if request.method == 'GET':
        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        supplier = Supplier.objects.get(sup_id=request.data['sup'])
        bill = Bill(
            total_amount=request.data['total_amount'],
            sup=supplier
        )
        bill.save()
        bill = Bill.objects.get(bill_no=Bill.objects.latest('bill_no').bill_no)
        # print(request.data['items'], bill)
        for items in request.data['items']:
            item = InventoryItems.objects.get(itemid=items['itemid'])
            item.total_quantity += items['total_quantity']
            item.save()
            has = Has(bill_no=bill, itemid=item, quantity=items['total_quantity'], price=items['price'])
            has.save()
        return Response(None, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def show_customer(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def show_inventory_items(request):
    if request.method == 'GET':
        inventoryitems = InventoryItems.objects.all()
        serializer = InventoryItemsSerializer(inventoryitems, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(request.data)
        serializer = InventoryItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def ShowFoodItems(request):
    fooditems = FoodItems.objects.all()
    serializer = FoodItemsSerializer(fooditems, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def ShowOrders(request):
    if request.method == 'GET':
        orders = AllOrders.objects.raw(
            'select order_id, name, phone, amount, payment_status from orders o, customer c where c.customer_ID = o.customer_ID;')
        serializer = AllOrdersSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NewOrderSerializer(data=request.data)
        if serializer.is_valid():
            if Customer.objects.filter(phone=serializer.data.get('phone')).exists():
                customer = Customer.objects.filter(phone=serializer.data.get('phone')).values('customer_id')[0][
                    'customer_id']
                order = Orders(
                    customer_id=customer,
                    payment_status=serializer.data.get('payment_status'),
                    payment_mode=serializer.data.get('payment_mode'),
                    staff_id=1,
                    amount=serializer.data.get('amount')
                )
                order.save()
            else:
                customer = Customer(
                    name=serializer.data.get('name'),
                    phone=serializer.data.get('phone')
                )
                customer.save()
                order = Orders(
                    customer_id=Customer.objects.latest('customer_id').customer_id,
                    payment_status=serializer.data.get('payment_status'),
                    payment_mode=serializer.data.get('payment_mode'),
                    staff_id=1,
                    amount=serializer.data.get('amount')
                )
                order.save()
            for i in serializer.data.get('order'):
                contain = Contains(
                    food=FoodItems.objects.filter(food_id=i['food_id'])[0],
                    quantity=i['quantity'],
                    order=Orders.objects.latest('order_id')
                )
                contain.save()
        retOrder = AllOrders(
            order_id=Orders.objects.latest('order_id').order_id,
            name=serializer.data.get('name'),
            phone=serializer.data.get('phone'),
            payment_status=Orders.objects.latest('order_id').payment_status,
            amount=Orders.objects.latest('order_id').amount
        )
        return Response(
            AllOrdersSerializer(AllOrders(
                order_id=Orders.objects.latest('order_id').order_id,
                name=serializer.data.get('name'),
                phone=serializer.data.get('phone'),
                payment_status=Orders.objects.latest('order_id').payment_status,
                amount=Orders.objects.latest('order_id').amount
            )).data,
            status=status.HTTP_201_CREATED
        )


@api_view(['POST'])
def ToggleOrder(request):
    # print(request.data)
    order = Orders.objects.get(order_id=request.data['order_id'])
    order.payment_status = 'paid'
    order.save()
    return Response(None, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def ShowStaff(request):
    if request.method == 'GET':
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        request.data['dob'] = request.data['dob'][:10]
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        # print(serializer.data)
        return Response(None, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def ShowSupplier(request):
    if request.method == 'GET':
        supplier = Supplier.objects.all()
        serializer = SupplierSerializer(supplier, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def ShowContains(request):
    contains = Contains.objects.all()
    serializer = ContainsSerializer(contains, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ShowHas(request):
    has = Has.objects.all()
    serializer = HasSerializer(has, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ShowStaffAbsentDays(request):
    staffabsentdays = StaffAbsentDays.objects.all()
    serializer = StaffAbsentDaysSerializer(staffabsentdays, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ShowTakesFrom(request):
    takesfrom = TakesFrom.objects.all()
    serializer = TakesFromSerializer(takesfrom, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def ShowAllStaff(request):
    if request.method == 'GET':
        staff = StaffList.objects.raw(
            'SELECT s.staff_id, s.first_name, s.last_name, s.phone, COUNT(sba.absent_days) AS no_absent_days, s.salary FROM staff s LEFT JOIN staff_absent_days sba ON sba.staff_id = s.staff_id AND MONTH(sba.absent_days) = MONTH(CURRENT_DATE) GROUP BY s.staff_id;')
        serializer = StaffListSerializer(staff, many=True)
        # print(serializer.data)
        return Response(serializer.data)
    elif request.method == 'POST':
        for i in request.data:
            ab = StaffAbsentDays(
                absent_days=datetime.datetime.now().date(),
                staff=Staff.objects.get(staff_id=i['staff_id'])
            )
            ab.save()
        return Response(None, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def PayStaff(request):
    payment = StaffPayment(
        amount=request.data['salary'],
        staff_id=request.data['staff_id'],
        date=datetime.datetime.now().date()
    )
    payment.save()
    # print(payment)
    return Response(None, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def G1Data(request):
    bill = BillSummary.objects.raw('SELECT b.month, b.sum + sp.sum AS expense, o.sum AS income FROM (SELECT MONTHNAME(date) AS month, SUM(total_amount) AS sum FROM bill GROUP BY MONTH(date)) b, (SELECT MONTHNAME(date) AS month, SUM(amount) AS sum FROM staff_payment GROUP BY month(date)) sp, (SELECT MONTHNAME(date_time) AS month, SUM(amount) AS sum FROM orders GROUP BY MONTH(date_time)) o WHERE b.month = sp.month AND b.month = o.month;')
    bill = BillSummarySerializer(bill, many=True)
    # print(bill.data)
    return Response(bill.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def G2Data(request):
    data = ExpSummary.objects.raw('SELECT i.category AS cat, SUM(h.price) AS sum FROM has h, bill b, inventory_items i WHERE h.bill_no = b.bill_no AND i.itemID = h.itemID GROUP BY i.category;')
    data = ExpSummarySerializer(data, many=True)
    # print(data.data)
    return Response(data.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def Avg(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(DISTINCT DATE(date_time))/COUNT(*) AS avg FROM orders;')
        row = cursor.fetchone()
        # print(row[0])
    return Response(row[0], status=status.HTTP_200_OK)

@api_view(['GET'])
def PDish(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT MAX(c.count) AS timer, name FROM (SELECT COUNT(*) AS count, food_id FROM contains GROUP BY food_id) c, food_items WHERE c.food_id = food_items.food_id;')
        row = cursor.fetchone()
        # print(row[1])
    return Response(row[1], status=status.HTTP_200_OK)

@api_view(['GET'])
def Tcus(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM orders WHERE DATE(date_time) = DATE(CURRENT_DATE);')
        row = cursor.fetchone()
        # print(row[1])
    return Response(row[0], status=status.HTTP_200_OK)

@api_view(['POST'])
def UpdateInventory(request):
    item = InventoryItems.objects.get(itemid=request.data['itemid'])
    item.total_quantity = request.data['total_quantity']
    item.save()
    return Response(None, status=status.HTTP_201_CREATED)
