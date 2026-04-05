from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
from users.permissions import IsAnalystRole

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

class AnalystTransactionView(APIView):
    permission_classes = [IsAuthenticated, IsAnalystRole]

    def get(self, request):
        queryset = Transaction.objects.all()
        city = request.query_params.get('city')
        t_type = request.query_params.get('type')
        min_amount = request.query_params.get('min_amount')

        if city:
            queryset = queryset.filter(user__city__iexact=city)
        if t_type:
            queryset = queryset.filter(transaction_type=t_type)
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        serializer = TransactionSerializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "results": serializer.data
        })