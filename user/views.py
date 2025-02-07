from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import MyUser
from courses.models import Course
from .forms import RegistrationForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Achievement, Coin
from django.urls import reverse


class UserCreateView(CreateView):
    model = MyUser
    template_name = 'registration/registration_form.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class UserProfileView(DetailView):
    model = MyUser
    template_name = 'user/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        posts = Course.objects.filter(owner=profile)
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = UserProfileForm
    template_name = 'user/edit_profile.html'

    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        # Динамически генерируем URL с username текущего пользователя
        return reverse('user:user_profile', kwargs={'username': self.request.user.username})
    

class AchievementListView(ListView):
    model = Achievement
    template_name = 'user/achievements.html'
    context_object_name = 'achievements'

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)


class CoinListView(ListView):
    model = Coin
    template_name = 'user/coins.html'
    context_object_name = 'coins'

    def get_queryset(self):
        return Coin.objects.filter(user=self.request.user)
    
