from django.urls import path
from .views import AIAdvisorView, AISummaryView

urlpatterns = [
    path('<int:pk>/', AIAdvisorView.as_view(), name='ai_advisor'),
    path('getsummary/', AISummaryView.as_view(), name='ai_summary_view'),  
]