from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from logic.models import Office, Clients, Orders, Suppliers, Products, Equipment, OfficeEquipment, DiscountCards,\
                         ProductsOffice
from logic.serializers import OfficeSerializer, ClientsSerializer, OrdersSerializer, SuppliersSerializer, \
                              ProductsSerializer, EquipmentSerializer, OrdersGetSerializer, OrdersGetInPeriod,\
                              EquipmentInOfficeSerializer, OrdersInOffice, OfficeId, Price, DiscountCardsSerializer, \
                              ClientsWithDiscountSerializer, ProductsOfficeSerializer, EquipmentType, \
                              GetOrdersAmountInPhotocenterSerializer

from datetime import datetime
from db.queries import DataBase


class OfficeView(ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    filter_backends = (filters.OrderingFilter,)


class OrdersView(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersGetSerializer
    filter_backends = (filters.OrderingFilter,)

    def create(self, request, *args, **kwargs):
        serializer = OrdersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['order_date'] = datetime.now()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersGetInPeriodView(ModelViewSet):
    serializer_class = OrdersGetInPeriod
    http_method_names = ['post']

    def get_queryset(self):
        return None

    def create(self, request, *args, **kwargs):
        serializer = OrdersGetInPeriod(data=request.data)
        db = DataBase()
        if serializer.is_valid():
            start_time = serializer.data['start_time']
            end_time = serializer.data['end_time']
            df = db.get_orders_in_period(start_time, end_time)
            db.close()
            return Response(df.to_dict(orient='records'))
        else:
            return Response(status.HTTP_404_NOT_FOUND)


class OrdersInOfficeView(ModelViewSet):
    serializer_class = OrdersInOffice
    http_method_names = ['post']

    def get_queryset(self):
        return None

    def create(self, request, *args, **kwargs):
        serializer = OrdersInOffice(data=request.data)
        db = DataBase()
        if serializer.is_valid():
            office_type = serializer.data['office_type']
            start_time = serializer.data['start_time']
            end_time = serializer.data['end_time']
            df = db.get_amount_of_orders_in_office_type(office_type, start_time, end_time)
            db.close()
            return Response(df.to_dict(orient='records'))
        else:
            return Response(status.HTTP_404_NOT_FOUND)


class OrdersInOfficeByIdView(ModelViewSet):
    serializer_class = OfficeId
    http_method_names = ['post']

    def get_queryset(self):
        return None

    def create(self, request, *args, **kwargs):
        serializer = OfficeId(data=request.data)
        db = DataBase()
        if serializer.is_valid():
            office_id = serializer.data['office_id']
            df = db.get_orders_in_office_by_id(office_id)
            db.close()
            return Response(df.to_dict(orient='records'))
        else:
            return Response(status.HTTP_404_NOT_FOUND)


class OrdersWithPriceBiggerView(ModelViewSet):
    serializer_class = Price
    http_method_names = ['post']

    def get_queryset(self):
        return None

    def create(self, request, *args, **kwargs):
        serializer = Price(data=request.data)
        db = DataBase()
        if serializer.is_valid():
            price = serializer.data['price']
            df = db.get_orders_with_price_bigger(price)
            db.close()
            return Response(df.to_dict(orient='records'))
        else:
            return Response(status.HTTP_404_NOT_FOUND)


class OrdersInPhotocenter(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetOrdersAmountInPhotocenterSerializer

    def get_queryset(self):
        db = DataBase()
        df = db.get_amount_of_orders_in_photocenter()
        db.close()
        return df.to_dict(orient='records')


class AmountOfEquipment(ModelViewSet):
    serializer_class = EquipmentType
    http_method_names = ['post']

    def get_queryset(self):
        return None

    def create(self, request, *args, **kwargs):
        serializer = EquipmentType(data=request.data)
        db = DataBase()
        if serializer.is_valid():
            equipment_type = serializer.data['equipment_type']
            df = db.get_amount_of_equipment(equipment_type)
            db.close()
            return Response(df.to_dict(orient='records'))
        else:
            return Response(status.HTTP_404_NOT_FOUND)


class ClientsView(ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    filter_backends = (filters.OrderingFilter,)


class DiscountCardsView(ModelViewSet):
    queryset = DiscountCards.objects.all()
    serializer_class = DiscountCardsSerializer
    filter_backends = (filters.OrderingFilter,)


class ClientsWithDiscountView(ModelViewSet):
    serializer_class = ClientsWithDiscountSerializer
    http_method_names = ['post', 'get']

    def get_queryset(self):
        db = DataBase()
        df = db.get_clients_and_cards()
        return df.to_dict(orient='records')

    def create(self, request, *args, **kwargs):
        serializer = ClientsWithDiscountSerializer(data=request.data)
        db = DataBase()
        if serializer.is_valid():
            description = serializer.data['description']
            discount = serializer.data['discount']
            df = db.get_number_of_clients_with_discount(description, discount)
            db.close()
            return Response(df.to_dict(orient='records'))
        else:
            return Response(status.HTTP_404_NOT_FOUND)


class ProductsView(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = (filters.OrderingFilter,)


class ProductsOfficeView(ModelViewSet):
    queryset = ProductsOffice.objects.all()
    serializer_class = ProductsOfficeSerializer
    filter_backends = (filters.OrderingFilter,)


class SuppliersView(ModelViewSet):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer
    filter_backends = (filters.OrderingFilter,)


class EquipmentView(ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = (filters.OrderingFilter,)


class EquipmentInOfficeView(ModelViewSet):
    queryset = OfficeEquipment.objects.all()
    serializer_class = EquipmentInOfficeSerializer
    filter_backends = (filters.OrderingFilter,)
