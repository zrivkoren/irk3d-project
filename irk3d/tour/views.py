from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator

from config.settings import EMAIL_HOST_USER, EMAIL_TO
from tour.models import Tour, Tag, Feedback, Service, Client, FAQ, Irk3dSettings, Contact
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
        "contact_form": ContactForm(),
    }
    if request.method == 'POST':
        form = ContactForm(request.POST)

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

    return render(request, template, context)


class ContactFormView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip
