from django.views.generic import ListView, DetailView
from .models import Course, Module, DepartmentProfile, Lesson
from courses.models import Subject
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Lesson
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Пагинация
        courses = Course.objects.all()
        paginator = Paginator(courses, 10)  # 10 курсов на страницу
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Добавление данных в контекст
        subjects = Subject.objects.all()  # Получаем все предметы
        context['page_obj'] = page_obj
        context['subjects'] = subjects
        
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'


class ModuleDetailView(DetailView):
    model = Module
    template_name = 'courses/module_detail.html'
    context_object_name = 'module'


class ProfileListView(ListView):
    model = DepartmentProfile
    template_name = 'profiles/profile_list.html'


class SubjectListView(ListView):
    template_name = 'profiles/subject_list.html'
    model = Course

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        return Subject.objects.filter(profile_id=profile_id)
    

class LessonListView(ListView):
    template_name = 'subjects/lesson_list.html'

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Lesson.objects.filter(module__course__subject_id=subject_id)
    
class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'


class LessonTestView(DetailView):
    model = Lesson
    template_name = 'courses/lesson_test.html'
    context_object_name = 'lesson'

    def get(self, request, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'])
        if not lesson.test:
            return redirect('courses:lesson_detail', pk=lesson.pk)
        return super().get(request, *args, **kwargs)


class SubmitTestView(View):
    def post(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        
        # Обработка данных формы
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                answers[question_id] = value  # или список, если multiple_choice

        # Логика проверки теста и сохранения результата
        # Например:
        score = 0  # Подсчёт баллов
        for question_id, answer in answers.items():
            # Сравниваем с правильными ответами (логика зависит от структуры ваших данных)
            pass

        messages.success(request, "Ваши ответы были отправлены! Вы набрали {} баллов.".format(score))
        return redirect('courses:lesson_detail', pk=lesson.id)