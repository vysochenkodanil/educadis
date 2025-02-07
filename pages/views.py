from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import FeedbackForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import StaticPage, Activity
from .forms import StaticPageForm, ActivityForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.http import HttpResponseForbidden
from .models import Activity, Comment
from django.utils.text import slugify
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Activity, ActivityRegistration
from .forms import ActivityRegistrationForm



class AddCommentView(View):
    def post(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        text = request.POST.get('text')
        Comment.objects.create(activity=activity, author=request.user, text=text)
        return redirect('pages:activity_detail', slug=activity.slug)

class EditCommentView(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return HttpResponseForbidden()
        return render(request, 'pages/edit_comment.html', {'comment': comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return HttpResponseForbidden()
        comment.text = request.POST.get('text')
        comment.save()
        return redirect('pages:activity_detail', slug=comment.activity.slug)

class DeleteCommentView(View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return HttpResponseForbidden()
        comment.delete()
        return redirect('pages:activity_detail', slug=comment.activity.slug)

def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


from django.views.generic import TemplateView
from .models import StaticPage, Activity

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pages'] = StaticPage.objects.all()
        context['activities'] = Activity.objects.all()[:5]  # Например, последние 5 активностей
        return context


class StaticPageDetailView(DetailView):
    model = StaticPage
    template_name = 'pages/static_page_detail.html'
    context_object_name = 'page'

class StaticPageCreateView(LoginRequiredMixin, CreateView):
    model = StaticPage
    form_class = StaticPageForm
    template_name = 'pages/static_page_form.html'
    success_url = reverse_lazy('pages:static_page_list')

class StaticPageUpdateView(LoginRequiredMixin, UpdateView):
    model = StaticPage
    form_class = StaticPageForm
    template_name = 'pages/static_page_form.html'
    success_url = reverse_lazy('pages:static_page_list')


class ActivityListView(ListView):
    model = Activity
    template_name = 'pages/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 15

class ActivityDetailView(DetailView):
    model = Activity
    template_name = 'pages/activity_detail.html'
    context_object_name = 'activity'

# class ActivityCreateView(LoginRequiredMixin, CreateView):
#     model = Activity
#     form_class = ActivityForm
#     template_name = 'pages/activity_form.html'
#     success_url = reverse_lazy('pages:activity_list')

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

class ActivityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'pages/activity_form.html'
    success_url = reverse_lazy('pages:activity_list')


    def test_func(self):
        # Только пользователи is_staff могут создавать активности
        return self.request.user.is_staff

    def form_valid(self, form):
        # Устанавливаем автора активности перед сохранением
        form.instance.author = self.request.user
        return super().form_valid(form)

class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'pages/activity_form.html'
    success_url = reverse_lazy('pages:activity_list')

@method_decorator(login_required, name='dispatch')
class ActivitySignupView(View):
    def get(self, request, slug):
        activity = get_object_or_404(Activity, slug=slug)
        
        # Проверяем, не записан ли уже пользователь
        if ActivityRegistration.objects.filter(user=request.user, activity=activity).exists():
            messages.warning(request, "Вы уже записаны на это мероприятие")
            return redirect('pages:activity_detail', slug=slug)
            
        form = ActivityRegistrationForm()
        return render(request, 'pages/activity_signup_form.html', {
            'activity': activity,
            'form': form
        })

    def post(self, request, slug):
        activity = get_object_or_404(Activity, slug=slug)
        form = ActivityRegistrationForm(request.POST)
        
        if form.is_valid():
            # Создаем запись, но не сохраняем в БД
            registration = form.save(commit=False)
            
            # Привязываем к пользователю и мероприятию
            registration.user = request.user
            registration.activity = activity
            
            # Сохраняем в БД
            registration.save()
            
            messages.success(request, "Вы успешно записаны на мероприятие!")
            return redirect('pages:activity_detail', slug=slug)
            
        # Если форма невалидна, показываем ошибки
        return render(request, 'pages/activity_signup_form.html', {
            'activity': activity,
            'form': form
        })
    



class FeedbackView(FormView):
    template_name = 'pages/feedback.html'  # Укажите путь к вашему шаблону
    form_class = FeedbackForm
    success_url = '/pages/feedback/'  # После успешной отправки останемся на той же странице

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        messages.success(self.request, "Ваше сообщение успешно отправлено!")
        return super().form_valid(form)
