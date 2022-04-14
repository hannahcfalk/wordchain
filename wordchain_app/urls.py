from django.urls import path

from . import views

app_name = 'wordchain'

urlpatterns = [
    path('', views.play, name='play'),
    path('account/', views.account, name='account'),
    path('about/', views.about, name='about'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('update_account_details/', views.update_account_details, name='update_account_details'),
    path('stats/', views.stats, name='stats')
]