from django import forms
from .models import StaticPage, Activity, ActivityRegistration
from django.utils.timezone import now
from django.utils import timezone


class StaticPageForm(forms.ModelForm):
    class Meta:
        model = StaticPage
        fields = ['title', 'slug', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False  # Слаг будет генерироваться автоматически


class ActivityForm(forms.ModelForm):
    date = forms.DateField(
        label="Дата проведения",
        widget=forms.DateInput(attrs={"type": "date"}),  # HTML5 поле для выбора даты
    )

    class Meta:
        model = Activity
        fields = ['title', 'content', 'date']  # Исключите 'slug'

    def clean_date(self):
        """
        Валидатор для проверки, что дата не находится в прошлом.
        """
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise forms.ValidationError("Дата активности не может быть в прошлом.")
        return date
    
class ActivityRegistrationForm(forms.ModelForm):
    class Meta:
        model = ActivityRegistration
        fields = ['additional_participants']
        widgets = {
            'additional_participants': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Иван Иванов, Мария Петрова...'
            }),
        }
        labels = {
            'additional_participants': "Дополнительные участники"
        }


class FeedbackForm(forms.Form):
    '''обработка обратной связи'''
    name = forms.CharField(
        max_length=100,
        label="Ваше имя",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        label="Ваш email",
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        )
    )
