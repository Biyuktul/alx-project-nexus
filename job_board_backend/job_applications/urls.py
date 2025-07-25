from django.urls import path

from .views import ApplicationDetailView, ApplicationListView

urlpatterns = [
    path('', ApplicationListView.as_view(), name='application'),
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
]