from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.CatalogListView.as_view()),
    path('cap-detail/<int:pk>/', views.CapDetailView.as_view()),
    path('home-page/', views.HomePageView.as_view()),
    path('order/', views.OrderListCreateView.as_view())
]

