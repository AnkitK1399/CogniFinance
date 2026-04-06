import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.permissions import IsAnalystRole, IsAdminRole
from django.conf import settings
from django.shortcuts import get_object_or_404
from users.models import User
from transactions.models import Transaction
from .models import AISummary
from django.core.mail import EmailMessage
from .serializers import AISummarySerializer
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

# Configure Gemini with your API Key
genai.configure(api_key=settings.GEMINI_API_KEY)

class AIAdvisorView(APIView):
    permission_classes = [IsAuthenticated, (IsAnalystRole|IsAdminRole)]

    def post(self, request, pk):
        
        user = User.objects.get(pk=pk)
        transactions = Transaction.objects.filter(user = user.id).order_by('-created_at')[:20]
        
        transaction_history = ""
        for tx in transactions:
            transaction_history += f"- {tx.date}: {tx.transaction_type} of {tx.amount} for {tx.category} ({tx.description}). Balance after: {tx.balance_snapshot}\n"

        prompt = f"""
        You are 'Cogni-Coach', a witty and expert financial advisor.
        
        User Profile:
        - Name: {user.username}
        - Occupation: {user.occupation if hasattr(user, 'occupation') else 'Professional'}
        - Current Balance: {user.current_balance}
        
        Recent Transaction History (Last 3):
        {transaction_history}
        
        Your Mission:
        1. Compare Income vs Expenses in this list. If Expenses > Income, give a polite 'wake-up call'.
        2. Identify 2 specific 'doable' expense cuts based on descriptions (e.g., if you see 'Coffee' or 'Netflix').
        3. Suggest 3 side-hustle opportunities specifically for a {user.occupation} living in {user.city}.
        
        Tone: Grounded, encouraging, but direct. Use Markdown for formatting.
        """

        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        print(response.text)
        AISummary.objects.create(user=user,ai_summary=response.text)
        mail_subject = 'AI summary for last 20 transaction records'
        message = f"""
                    Hi {user.username},

                    Your latest financial breakdown and custom "Cogni-Coach" advice are now available.

                    We’ve analyzed your recent transactions to help you optimize your spending and find new income opportunities.

                    Log In to View Summary 

                    Stay on track,
                    The CogniFinance Team


                    """
        to_mail = user.email
        send_mail = EmailMessage(mail_subject, message, to=[to_mail])
        send_mail.send()

        return Response({
            "coach_advice": response.text,
            "user_status": "Overspending" if user.current_balance < 1000 else "Stable"
        },status=201)

class UserPagination(PageNumberPagination):
    max_page_size = 50
    page_size = 50
    page_size_query_param = 'size'


class AISummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f"UserView:{request.get_full_path()}"
        cache_response = cache.get(cache_key)
        if cache_response:
            return Response(cache_response,status=200)
        summaries = AISummary.objects.filter(user=request.user).order_by('-created_at')
        userpagination = UserPagination()
        paginated_data = userpagination.paginate_queryset(summaries,request=request)
        serializer = AISummarySerializer(paginated_data, many=True)
        response = userpagination.get_paginated_response(serializer.data).data
        cache.set(cache_key,response,timeout=60*60)
        return Response(response,status=200)



from rest_framework import status
from django.shortcuts import get_object_or_404

class AISummaryDetailView(APIView):
    """
    Handles retrieving and deleting a single AI Summary by ID.
    Accessible only by Admin and Analyst roles.
    """
    permission_classes = [IsAuthenticated, (IsAnalystRole | IsAdminRole)]

    def get(self, request, pk):
        summary = get_object_or_404(AISummary, pk=pk)
        serializer = AISummarySerializer(summary)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        summary = get_object_or_404(AISummary, pk=pk)
        summary.delete()
        cache.clear() 
        return Response({
            "message": f"Summary ID {pk} deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)