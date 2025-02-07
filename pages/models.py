from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now



class StaticPage(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'статическая страница'
        verbose_name_plural = 'Статические страницы'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:static_page_detail', kwargs={'slug': self.slug})


class Activity(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Идентификатор'
    )
    content = models.TextField(verbose_name='Содержание', help_text='Описание мероприятия.')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    date = models.DateField(default=now, verbose_name='Дата мероприятия')

    class Meta:
        verbose_name = 'активность'
        verbose_name_plural = 'Активности'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Activity.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:activity_detail', kwargs={'slug': self.slug})
    
class ActivityRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    additional_participants = models.TextField(
        blank=True,
        null=True,
        verbose_name="Дополнительные участники",
        help_text="Перечислите имена участников через запятую"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'activity']  # Запрещаем повторные записи



class Comment(models.Model):
    activity = models.ForeignKey('Activity', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} - {self.text[:20]}"
