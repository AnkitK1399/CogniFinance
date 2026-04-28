from django.urls import path
from .views import TransactionView, AnalystTransactionView

urlpatterns = [
    path('add_view/', TransactionView.as_view(), name='add_transaction'),
    path('update_delete/<int:pk>/', TransactionView.as_view(), name='update_transaction'),
    path('analystView/', AnalystTransactionView.as_view(), name="analyst_view"),
   
]