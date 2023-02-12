from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('about/', views.about, name='about'),
     path('photos/', views.photos_index, name="index"),
     path('photos/<int:photo_id>/', views.photos_detail, name="detail"),
     path('photos/create/', views.create_photo, name='photos_create'),
     path('photos/<int:photo_id>/delete/', views.photos_delete, name='photos_delete'),
     path('photos/<int:pk>/update/', views.PhotoUpdate.as_view(), name='photos_update'),
     path('photoscontext/<int:pk>/update/', views.PhotoContextUpdate.as_view(), name='context_update'),
     path('accounts/signup/', views.signup, name='signup'),
     path('profile/', views.profile, name='users-profile'),
     path('profile/password-change/', views.ChangePasswordView.as_view(), name='password_change'),
     path('profile/<str:username>/', views.profile_detail, name='profile_detail')
]