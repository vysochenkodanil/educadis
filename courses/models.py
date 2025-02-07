from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()


class Subject(models.Model):
    title = models.CharField(max_length=settings.TITLE_MAX_LENGTH,
        verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=settings.TITLE_MAX_LENGTH,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        )
    )
    profile = models.ForeignKey(
        'courses.DepartmentProfile',
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name='Профиль обучения',
        null=True,  # Если данные не обязательны
        blank=True  # Если поле может быть пустым
    )

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'Предмет'

    def __str__(self):
        return self.title[:settings.TITLE_MAX_LENGTH]


class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE,
        verbose_name='предмет'
        )
    title = models.CharField(max_length=settings.TITLE_MAX_LENGTH)
    slug = models.SlugField(
        max_length=settings.TITLE_MAX_LENGTH,
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        )
    )
    overview = models.TextField(verbose_name='Описание')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создания'
        )
    
    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'Курс'

    def __str__(self):
        return self.title[:settings.TITLE_MAX_LENGTH]
    

class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name='modules',
        on_delete=models.CASCADE,
        verbose_name='курс'
    )
    title = models.CharField(
        max_length=settings.TITLE_MAX_LENGTH,
        verbose_name='Заголовок'
        )
    description = models.TextField(blank=True,  verbose_name='Описание')
    
    def __str__(self):
        return self.title[:settings.TITLE_MAX_LENGTH]
    

class Lesson(models.Model):
    module = models.ForeignKey(
        Module,
        related_name='lessons',
        on_delete=models.CASCADE,
        verbose_name='Модуль'
    )
    title = models.CharField(max_length=settings.TITLE_MAX_LENGTH, verbose_name='Название урока')
    content = models.TextField(verbose_name='Теоретическая часть')
    test = models.TextField(blank=True, null=True, verbose_name='Тестовое задание')  # Поле необязательно

    def __str__(self):
        return self.title[:settings.TITLE_MAX_LENGTH]

class DepartmentProfile(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название профиля")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name
    
class LessonProgress(models.Model):
    user = models.ForeignKey(
        User,
        related_name='lesson_progress',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name='progress',
        on_delete=models.CASCADE,
        verbose_name='Урок'
    )
    completed = models.BooleanField(default=False, verbose_name='Завершён')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Завершён' if self.completed else 'Не завершён'}"