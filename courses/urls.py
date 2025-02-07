from django.urls import path
from .views import CourseListView, CourseDetailView, ModuleDetailView
from . import views


app_name = 'courses'
urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<slug:course_slug>/<slug:module_slug>/', ModuleDetailView.as_view(), name='module_detail'),
    path('profiles/', views.ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:profile_id>/subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/<int:subject_id>/modules/', views.LessonListView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/<int:pk>/test/', views.LessonTestView.as_view(), name='lesson_test'),
    path('module/<int:pk>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('lesson/<int:pk>/test/submit/', views.SubmitTestView.as_view(), name='submit_test'),
]