# NewsCentral/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('ApiAdmin/ListAll/', views.ListStocks.as_view()),
    path('ApiAdmin/ListAlllinks/', views.ListLINKS.as_view()),
    path('<str:pk>/', views.DetailStocks.as_view()),

    path('test/trylogger/', views.index),
    path('PostValidatedStock', views.PostValidatedStock.PostStock),
    path('linkcreation', views.PostMethodLink.post_LINK),
    # path('query/<str:StockId>/', views.GETMethod.QueryStock),

]