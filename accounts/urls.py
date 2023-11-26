from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterPage, name='RegisterPage'),
    path('', LoginPage, name='LoginPage'),
    path('logout/', logout, name='logout'),
    path('home/', HomePage, name='HomePage'),
    path('upload/', VideoUploadView.as_view(), name='UploadPage'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video_detail'),
    path('profile/<str:username>', ProfilePage, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('profile/edit-video/<int:pk>/', edit_video_profile, name='edit_video_profile'),
    path('profile/video/<int:pk>/delete/', delete_profile_video, name='delete_profile_video'),
    path('search/', search_results, name='search_results'),

    path('mod/allvideos', ListViewAdmin, name='ModList'),
    path('mod/allusers', ListViewAdminUsers, name='ModListUsers'),
    path('videos/<int:pk>/delete/', delete_video, name='delete_video'),
    path('videos/<int:pk>/edit/', edit_video, name='edit_video'),
    path('profile/<int:pk>/edit/', edit_user, name='edit_user'),
    path('profile/delete/<int:pk>/', delete_profile, name='delete_profile'),
]