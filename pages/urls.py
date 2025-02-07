from django.urls import path
from django.views.generic import TemplateView
from .views import (
    StaticPageDetailView, StaticPageCreateView, StaticPageUpdateView,
    ActivityListView, ActivityDetailView, ActivityCreateView, ActivityUpdateView, FeedbackView,
    AddCommentView, EditCommentView, DeleteCommentView, ActivitySignupView
)


app_name = 'pages'
urlpatterns = [
    # Статические страницы
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('rules/', TemplateView.as_view(template_name='pages/rules.html'), name='rules'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),

    # Динамические страницы
    # path('static/<slug:slug>/', StaticPageDetailView.as_view(), name='static_page_detail'),
    path('static/create/', StaticPageCreateView.as_view(), name='static_page_create'),
    path('static/<slug:slug>/update/', StaticPageUpdateView.as_view(), name='static_page_update'),

    # Активности
    path('activities/', ActivityListView.as_view(), name='activity_list'),
    path('activities/create/', ActivityCreateView.as_view(), name='activity_create'),
    path('activities/<slug:slug>/', ActivityDetailView.as_view(), name='activity_detail'),
    path('activities/<slug:slug>/update/', ActivityUpdateView.as_view(), name='activity_update'),
    path('activities/<slug:slug>/signup/', ActivitySignupView.as_view(), name='activity_signup'),

    #коменты
    path('activities/<int:activity_id>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('comments/<int:comment_id>/edit/', EditCommentView.as_view(), name='edit_comment'),
    path('comments/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
]