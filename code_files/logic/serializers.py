from rest_framework import serializers
from logic.models import Office, Clients, Orders, Suppliers, Products, Equipment, OfficeEquipment, DiscountCards,\
                         ProductsOffice


class OfficeSerializer(serializers.ModelSerializer):
    description = serializers.ChoiceField(choices=[('Главный', 'Главный'), ('Филиал', 'Филиал'), ('Киоск', 'Киоск')])

    class Meta:
        model = Office
        fields = [
            'id', 'address', 'description', 'working_places',
        ]


class ClientsSerializer(serializers.ModelSerializer):
    description = serializers.ChoiceField(choices=[('Профессионал', 'Профессионал'), ('Любитель', 'Любитель')])

    class Meta:
        model = Clients
        fields = [
            'id', 'discount_card', 'description'
        ]


class DiscountCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCards
        fields = [
            'number', 'discount'
        ]


class ClientsWithDiscountSerializer(serializers.Serializer):
    description = serializers.ChoiceField(choices=[('Профессионал', 'Профессионал'), ('Любитель', 'Любитель')])
    discount = serializers.IntegerField(allow_null=False, required=True)


class OrdersSerializer(serializers.ModelSerializer):
    format = serializers.ChoiceField(choices=[('10x15', '10x15'), ('15x20', '15x20'), ('21x30', '21x30'),
                                              ('9x12', '9x12'), ('13x18', '13x18')])

    paper_type = serializers.ChoiceField(choices=[('Глянцевая', 'Глянцевая'), ('Полуглянцевая', 'Полуглянцевая'),
                                                  ('Матовая', 'Матовая'), ('Шелковисто-матовая', 'Шелковисто-матовая')])

    class Meta:
        model = Orders
        fields = [
            'id', 'office', 'photos_amount', 'format', 'paper_type', 'urgency', 'price'
        ]


class OrdersGetSerializer(serializers.ModelSerializer):
    format = serializers.ChoiceField(choices=[('10x15', '10x15'), ('15x20', '15x20'), ('21x30', '21x30'),
                                              ('9x12', '9x12'), ('13x18', '13x18')])

    paper_type = serializers.ChoiceField(choices=[('Глянцевая', 'Глянцевая'), ('Полуглянцевая', 'Полуглянцевая'),
                                                  ('Матовая', 'Матовая'), ('Шелковисто-матовая', 'Шелковисто-матовая')])

    class Meta:
        model = Orders
        fields = [
            'id', 'office', 'photos_amount', 'format', 'paper_type', 'order_date', 'urgency', 'price'
        ]


class OfficeId(serializers.Serializer):
    office_id = serializers.IntegerField(required=True, allow_null=False)


class OrdersGetInPeriod(serializers.Serializer):
    start_time = serializers.DateField(required=True, allow_null=False)
    end_time = serializers.DateField(required=True, allow_null=False)


class OrdersInOffice(serializers.Serializer):
    office_type = serializers.ChoiceField(required=True, allow_null=False,
                                          choices=[('Главный', 'Главный'), ('Филиал', 'Филиал'), ('Киоск', 'Киоск'),
                                                   ('По всем', 'По всем')])
    start_time = serializers.DateField(required=True, allow_null=False)
    end_time = serializers.DateField(required=True, allow_null=False)


class GetOrdersAmountInPhotocenterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    address = serializers.CharField()
    description = serializers.CharField()
    amount_of_orders = serializers.IntegerField()


class Price(serializers.Serializer):
    price = serializers.FloatField(required=True, allow_null=False)


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = [
            'name', 'specialization',
        ]


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id', 'name', 'company',
        ]


class ProductsOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsOffice
        fields = [
            'id', 'product', 'office', 'amount'
        ]


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            'id', 'name', 'company',
        ]


class EquipmentType(serializers.Serializer):
    types = [(1, 'Студийный свет'), (2, 'Фотофон'), (3, 'Вспышка'), (4, 'Отражатели'), (5, 'Софтбокс'),
             (6, 'Фотозонт'), (7, 'Рефлектор')]

    equipment_type = serializers.ChoiceField(choices=types)


class EquipmentInOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeEquipment
        fields = [
            'id', 'equipment', 'office', 'amount'
        ]
