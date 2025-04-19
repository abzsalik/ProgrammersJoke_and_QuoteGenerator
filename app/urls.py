from django.urls import path 
from .views import *
urlpatterns = [
    path('',Home.as_view(),name="home"),
    path('quote/',Quote.as_view(),name="quote"),
]
