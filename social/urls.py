from django.urls import path
from . import views

app_name= 'social'

urlpatterns = [
    path('',views.show_login_page, name='login'),
    path('login/',views.show_login_page, name='login'),
    path('register/',views.show_register_page,name='register'),
    path('logout/',views.logout_page, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('search_profile/', views.search_profile, name='search_profile'),
    path('create_chat/',views.create_chat,name='create_chat'),
    path('send_invitation/<str:username>/',views.send_invitation,name='send_invitation'),
    path('handle_invitation/',views.handle_invitation,name='handle_invitation'),
    path('remove_friend/<str:username>/', views.remove_friend, name='remove_friend'),

]