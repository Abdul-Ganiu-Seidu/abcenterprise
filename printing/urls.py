from django.urls import path
from . import views

urlpatterns = [
    path('', views.printing_page, name='printing'),
    path('upload/', views.upload_print, name='upload_print'),
]