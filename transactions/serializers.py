from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    current_balance =serializers.ReadOnlyField(source = 'user.current_balance')
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'transaction_type', 'category', 'description', 'date','current_balance','balance_snapshot']
        read_only_fields = ['id', 'user']

    