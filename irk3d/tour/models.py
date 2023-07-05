from django.db import models


class Review(models.Model):
    text = models.TextField()
    author_name = models.CharField(max_length=100)
    author_position_company = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='reviews/')


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Scene(models.Model):
    name = models.CharField(max_length=160)
    name_for_deep_link = models.CharField(max_length=160, blank=True, null=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='scenes', blank=True, null=True)

    class Meta:
        verbose_name = 'панорама'
        verbose_name_plural = 'панорамы'

    def __str__(self):
        return self.name


class Tour(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    preview_image = models.ImageField(
        'Основное изображение тура',
        upload_to='tours/',
        blank=True
    )
    text = models.TextField()
    vt_url = models.CharField(max_length=160, help_text='URL исходники ВТ относительно ссылки на сайт', blank=True)
    tags = models.ManyToManyField(Tag, related_name='tour')
    is_deeplink = models.BooleanField(default=False)
    review = models.OneToOneField('Review', on_delete=models.CASCADE, related_name='tour_review', blank=True, null=True)
    yandex_map_url = models.URLField(blank=True, null=True)
    google_maps_url = models.URLField(blank=True, null=True)
    external_link = models.URLField(blank=True, null=True, help_text='Ссылка на тур на внешнем сайте')

    class Meta:
        verbose_name = 'тур'
        verbose_name_plural = 'туры'

    def __str__(self):
        return self.name

    def get_tags(self):
        return ",\n".join([t.name for t in self.tags.all()])
