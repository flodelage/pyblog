from django.urls import path

from blog import views

urlpatterns = [
    path('posts/', views.post_list, name='home'),
]