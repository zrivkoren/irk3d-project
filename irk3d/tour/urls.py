from django.urls import path
from . import views


urlpatterns = [
    path('api_tour_list/', views.api_tour_list),
    path('<str:tour_slug>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('tours/', views.AllToursListView.as_view(template_name='tour/all_tour_list.html'), name='all_tours'),
    path('tag/<str:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('', views.home, name='home'),

]
