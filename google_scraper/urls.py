from django.urls import path
from search import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download_csv/<str:keyword>/', views.download_csv, name='download_csv'),
]
