from django.urls import path
from .views import AIAdvisorView, AISummaryView, AISummaryDetailView, TexttoSQL

urlpatterns = [
    path('<int:pk>/', AIAdvisorView.as_view(), name='ai_advisor'),
    path('getsummary/', AISummaryView.as_view(), name='ai_summary_view'), 
    path('aisummary/<int:pk>/', AISummaryDetailView.as_view(), name='summary-detail'),
    path('text_to_sql/', TexttoSQL.as_view(), name='text_to_sql'),
]