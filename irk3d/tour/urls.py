from django.urls import path
from . import views

urlpatterns = [
    path('<str:tour_slug>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('tours/', views.AllToursListView.as_view(template_name='tour/all_tour_list.html'), name='all_tours'),
    path('tag/<str:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('', views.home),
]
