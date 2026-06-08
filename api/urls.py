from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),

    path('add-item/', add_item),
    path('items/', get_items),
    path('delete-item/<int:id>/', delete_item),

    path('create-invoice/', create_invoice),
    path('invoices/', get_invoices),
    path('delete-invoice/<int:id>/', delete_invoice),
]