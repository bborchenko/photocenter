from django.urls import path, include
from rest_framework import routers

import logic.views as views

app_name = 'reservations_api'

router = routers.DefaultRouter()
router.register(r'office', views.OfficeView, 'office')
router.register(r'orders', views.OrdersView, 'orders')
router.register(r'clients', views.ClientsView, 'clients')
router.register(r'discount_cards', views.DiscountCardsView, 'discount_cards')
router.register(r'equipment', views.EquipmentView, 'equipment')
router.register(r'suppliers', views.SuppliersView, 'suppliers')
router.register(r'products', views.ProductsView, 'products')
router.register(r'office_equipment', views.EquipmentInOfficeView, 'office_equipment')
router.register(r'office_products', views.ProductsOfficeView, 'office_products')
router.register(r'orders_in_period', views.OrdersGetInPeriodView, 'orders_in_period')
router.register(r'orders_amount_in_office', views.OrdersInOfficeView, 'amount_of_orders_in_office')
router.register(r'orders_amount_in_photocenter', views.OrdersInPhotocenter, 'amount_of_orders_in_photocenter')
router.register(r'orders_by_office_id', views.OrdersInOfficeByIdView, 'orders_by_office_id')
router.register(r'orders_with_price_bigger', views.OrdersWithPriceBiggerView, 'orders_with_price_bigger')
router.register(r'clients_with_discount', views.ClientsWithDiscountView, 'clients_with_discount')
router.register(r'equipment_amount_by_type', views.AmountOfEquipment, 'equipment_amount_by_type')

urlpatterns = [
    path('', include(router.urls)),
]
