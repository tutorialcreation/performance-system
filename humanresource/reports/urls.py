from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('api/data/', views.get_data, name='api_data'),
    path('api/chart/data/', views.ChartData.as_view()),
]
