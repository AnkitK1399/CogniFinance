from django.urls import path
from .views import TransactionView

urlpatterns = [
    path('add/', TransactionView.as_view(), name='add_transaction'),
    path('add/<int:pk>/', TransactionView.as_view(), name='update_transaction'),
   
]