from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from search import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download_csv/<str:keyword>/', views.download_csv, name='download_csv'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
