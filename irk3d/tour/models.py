from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse


class Feedback(models.Model):
    text = RichTextField()
    author_name = models.CharField(max_length=100)
    author_position_company = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='feedback/')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.author_position_company


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_in_portfolio = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tag_detail", kwargs={"slug": self.slug})


class Scene(models.Model):
    name = models.CharField(max_length=160)
    order = models.IntegerField(default=0)
    name_for_deep_link = models.CharField(max_length=160, blank=True, null=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='scenes', blank=True, null=True)

    class Meta:
        verbose_name = 'панорама'
        verbose_name_plural = 'панорамы'
        ordering = ['order']

    def __str__(self):
        return self.name


class Tour(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    created = models.DateField(blank=True, null=True)
    order = models.IntegerField(default=0)
    preview_image = models.ImageField(
        'Основное изображение тура',
        upload_to='tours/'
    )
    text = RichTextUploadingField()
    vt_url = models.CharField(
        max_length=160, help_text='URL исходников ВТ относительно ссылки на сайт', blank=True, null=True
    )
    tags = models.ManyToManyField(Tag, related_name='tour')
    is_deeplink = models.BooleanField(default=False)
    client = models.ForeignKey(
        'Client', on_delete=models.SET_NULL, related_name='tour_client', blank=True, null=True
    )
    feedback = models.ForeignKey(
        'Feedback', on_delete=models.SET_NULL, related_name='tour_feedback', blank=True, null=True
    )
    yandex_map_url = models.URLField(blank=True, null=True)
    google_maps_url = models.URLField(blank=True, null=True)
    external_link = models.URLField(blank=True, null=True, help_text='Ссылка на тур на внешнем сайте')

    class Meta:
        verbose_name = 'тур'
        verbose_name_plural = 'туры'
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_admin_tags(self):
        return ",\n".join([t.name for t in self.tags.all()])

    def get_absolute_url(self):
        return reverse("tour_detail", kwargs={"tour_slug": self.slug})

    def get_vt_url(self):
        if self.external_link:
            return self.external_link
        return reverse('home') + self.vt_url


class Service(models.Model):
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    text = RichTextField()
    icon_bi_class = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'
        ordering = ['order']

    def __str__(self):
        return self.name


class Client(models.Model):
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='clients-logo/')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['order']

    def __str__(self):
        return self.name


class FAQ(models.Model):
    number = models.IntegerField(default=1)
    question = models.CharField(max_length=200)
    answer = models.TextField()

    class Meta:
        ordering = ['number']
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'

    def __str__(self):
        return self.question


class Irk3dSettings(models.Model):
    price_low = models.IntegerField()
    price_medium = models.IntegerField()
    price_high = models.IntegerField()
    vt_count = models.IntegerField()
    panorama_count = models.IntegerField()


class Contact(models.Model):
    name = models.CharField(max_length=120)
    contact_info = models.CharField(max_length=140)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя', blank=True, null=True)
    content = models.TextField(verbose_name='Содержимое письма')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']

    def __str__(self):
        return f'Вам письмо от {self.contact_info}'
