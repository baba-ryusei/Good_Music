from django.contrib import admin
from django.urls import path
from app_reco.views import frontpage
from app_reco import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",frontpage),
    path('create-play/', views.create_play, name='create_play'),
    path('groups/', views.group_list, name='play_list'),
    path('group/<uuid:group_id>/', views.group_detail, name='play_detail'),
    path('delete-song/<int:song_id>/', views.delete_song, name='delete_song'),
    path('delete-artist/<int:song_id>/', views.delete_artist, name='delete_artist'),
    path('delete-group/<int:group_id>/', views.delete_group, name='delete_group'),
    path('like-song/<int:song_id>/', views.like_song, name='like_song')
]

