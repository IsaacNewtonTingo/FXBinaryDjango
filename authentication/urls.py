from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('account', views.account, name="account"),
    path('terms', views.terms, name="terms"),
    path('getStarted', views.getStarted, name="getStarted"),
    path('deposit', views.deposit, name="deposit"),
    path('withdraw', views.withdraw, name="withdraw"),


]
