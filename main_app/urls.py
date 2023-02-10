from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('about/', views.about, name='about'),
     path('photos/', views.photos_index, name="index"),
     path('photos/<int:photo_id>', views.photos_detail, name="detail"),
     path('photos/create/', views.PhotoCreate.as_view(), name='photos_create'),
     path('context/create/', views.PhotoContextCreate.as_view(), name='photo_context_create')
]