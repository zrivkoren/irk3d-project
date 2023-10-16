from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from config.settings import EMAIL_HOST_USER, EMAIL_TO
from tour.models import Tour, Tag, Feedback, Service, Client, FAQ, Irk3dSettings
from tour.forms import ContactForm
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


class TagDetailView(DetailView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'tour/tag_detail.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        tours = Tour.objects.filter(tags__in=[tag])
        paginator = Paginator(tours, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
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
    template_name = 'tour/tour_detail_v2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_tours'] = Tour.objects.order_by('-created')[:2]
        context['all_tags'] = Tag.objects.all().order_by('order')
        return context


def home(request):
    template = 'tour/home.html'
    context = {
        "latest_tours": Tour.objects.order_by('-created')[:3],
        "feedbacks": Feedback.objects.all()[::-1],
        "services": Service.objects.all().order_by('order'),
        "clients": Client.objects.all().order_by('order'),
        "faqs": FAQ.objects.all().order_by('number'),
        "tags": Tag.objects.filter(is_in_portfolio=True).order_by('order'),
        "settings": Irk3dSettings.objects.first(),
        "title": "Irk3D - Виртуальные туры и лучшие 3D панорамы",

    }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        context['form_is_bound'] = True

        if form.is_valid():
            contact = form.save(commit=False)
            contact.ip_address = get_client_ip(request)
            contact.save()
            text = f"""   Привет! Новое сообщение с сайта Irk3D
            Имя: {form.cleaned_data['name']} 
            Контактная информация: {form.cleaned_data['contact_info']} 
            Текст сообщения: 
            {form.cleaned_data['content']}"""

            try:
                send_mail(
                    'Сообщение с сайта Irk3D, форма обратной связи',
                    text,
                    EMAIL_HOST_USER,
                    [EMAIL_TO],
                    fail_silently=False,
                    auth_user=EMAIL_HOST_USER,
                    auth_password=EMAIL_HOST_PASSWORD
                )

            except Exception as e:
                print(e)
                return HttpResponseServerError(
                    f"{e} Ошибка сервера!  --- Отправка сообщения не удалась|")

            context['success'] = True
            return render(request, template, context)
        else:
            context["contact_form"] = form
            context['success'] = False
            return render(request, template, context)
    else:
        context["contact_form"] = ContactForm()

    return render(request, template, context)


def custom404(request, exception):
    return render(request, 'tour/404.html', status=404)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip
