from django.shortcuts import render
from django.views.generic import ListView, DetailView
from tour.models import Tour, Tag, Feedback, Service, Client


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
    template = 'tour/home.html'

    context = {
        "latest_tours": Tour.objects.order_by('-created')[:3],
        "feedbacks": Feedback.objects.all()[::-1],
        "services": Service.objects.all().order_by('order'),
        "clients": Client.objects.all().order_by('order'),
    }

    return render(request, template, context)
