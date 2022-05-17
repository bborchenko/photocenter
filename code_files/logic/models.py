from django.db import models


class Office(models.Model):
    id = models.IntegerField(null=False, unique=True, primary_key=True)
    address = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=7, null=False)
    working_places = models.IntegerField(null=False)


class KioskToOffice(models.Model):
    kiosk_id = models.IntegerField(null=False, unique=True, primary_key=True)
    office_id = models.IntegerField(null=False)


class Clients(models.Model):
    id = models.IntegerField(null=False, unique=True, primary_key=True)
    description = models.CharField(max_length=15, null=False)
    discount_card = models.IntegerField(unique=True)


class DiscountCards(models.Model):
    number = models.OneToOneField(to=Clients, on_delete=models.PROTECT, to_field='discount_card', primary_key=True)
    discount = models.IntegerField(null=False, default=10)


class Equipment(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=30, null=False, unique=True)
    company = models.CharField(max_length=30, null=False, unique=True)


class OfficeEquipment(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    equipment = models.ForeignKey(to=Equipment, on_delete=models.CASCADE, to_field='id')
    office = models.ForeignKey(to=Office, on_delete=models.CASCADE, to_field='id')
    amount = models.IntegerField(null=False, default=0)


class Orders(models.Model):
    id = models.IntegerField(null=False, unique=True, primary_key=True)
    office = models.ForeignKey(to=Office, on_delete=models.CASCADE, to_field='id')
    photos_amount = models.IntegerField(null=False)
    format = models.CharField(max_length=20, null=False)
    paper_type = models.CharField(max_length=20, null=False)
    order_date = models.DateTimeField(null=False)
    urgency = models.BooleanField(null=False, default=False)
    price = models.FloatField(null=False, default=0)


class Products(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=30, null=False, unique=True)
    company = models.CharField(max_length=30, null=False, unique=True)


class ProductsOffice(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, to_field='id')
    office = models.ForeignKey(to=Office, on_delete=models.CASCADE, to_field='id')
    amount = models.IntegerField(null=False, default=0)


class Suppliers(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, primary_key=True)
    specialization = models.CharField(max_length=30, null=False)
