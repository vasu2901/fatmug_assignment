from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    # path('accounts/profile/', views.logout_view, name='video_list'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/', views.display_video_with_search, name='display_video_with_search'),
    path('', views.video_list, name='video_list'),
]
