from django.shortcuts import render
from django.views.generic import ListView, DetailView
from tour.models import Tour, Tag

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from tour.serializers import TourListSerializer


class TagDetailView(DetailView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'tour/tag_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        context['tours'] = Tour.objects.filter(tags__in=[tag])
        return context


class AllToursListView(ListView):
    model = Tour
    context_object_name = 'all_tours'

    def get_queryset(self):
        return Tour.objects.all()


class TourDetailView(DetailView):
    model = Tour
    slug_url_kwarg = 'tour_slug'
    context_object_name = 'tour'


def home(request):
    return render(request, 'tour/home.html')


# @api_view(['GET'])
# def api_tour_list(request):
#     tours = Tour.objects.all()
#     serializer = TourListSerializer(tours, many=True)
#     return Response(serializer.data)


class TourListView(ListView):
    model = Tour

    def get_queryset(self):
        return Tour.objects.filter(tags__slug=self.kwargs.get('slug'))
