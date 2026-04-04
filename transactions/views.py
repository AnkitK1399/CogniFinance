from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404

class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user_transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(user_transactions, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        serializer = TransactionSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

        serializer = TransactionSerializer(transaction, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
        transaction.delete()
        return Response(
            {"message": "Transaction deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )