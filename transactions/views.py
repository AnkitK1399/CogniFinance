from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import get_object_or_404
from users.permissions import IsAnalystRole
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user_transactions = Transaction.objects.filter(user=request.user)
        record_pagination = StandardPagination()
        paginated_data = record_pagination.paginate_queryset(user_transactions,request=request) 
        serializer = TransactionSerializer(paginated_data, many=True)
        response = record_pagination.get_paginated_response(serializer.data).data

        return Response(response,status=200)

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
        queryset = Transaction.objects.all().order_by('-created_at')
        city = request.query_params.get('city')
        t_type = request.query_params.get('type')
        min_amount = request.query_params.get('min_amount')
        input_date = request.query_params.get('input_date')
        date_after = request.query_params.get('date_after')
        date_before = request.query_params.get('date_before')
        user_id = request.query_params.get('user_id')
        try:
            if city:
                queryset = queryset.filter(user__city__iexact=city)
            if t_type:
                queryset = queryset.filter(transaction_type=t_type)
            if min_amount:
                queryset = queryset.filter(amount__gte=min_amount)
            if input_date:
                queryset = queryset.filter(date=input_date)
            if date_after:
                queryset = queryset.filter(date__gte=date_after)
            if date_before:
                queryset = queryset.filter(date__lte=date_before)
            if user_id:
                queryset = queryset.filter(user=user_id)
            
        except Exception as e:
            return Response({'error':'query parameter value is wrong'}, status=400)

        record_pagination = StandardPagination()
        paginated_data = record_pagination.paginate_queryset(queryset,request=request) 
        serializer = TransactionSerializer(paginated_data, many=True)
        response = record_pagination.get_paginated_response(serializer.data).data

       # serializer = TransactionSerializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "results": response
        })