from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('<str:tour_slug>/', views.TourDetailView.as_view(), name='tour_detail'),
]
